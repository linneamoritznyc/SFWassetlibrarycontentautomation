/**
 * Wormhole <-> Google Doc sync.
 *
 * Bound to the "October 2026 Content (Wormhole)" doc. Runs as the person who
 * installs it, so Wormhole needs no Google credentials. Script Properties
 * (Project Settings > Script Properties) hold:
 *   WORMHOLE_URL         e.g. https://sf-wassetlibrarycontentautomation-web.vercel.app
 *   WORMHOLE_SYNC_TOKEN  the same value as WORMHOLE_SYNC_TOKEN in Vercel
 *   VERCEL_BYPASS        only while Wormhole runs on a protected preview URL:
 *                        Vercel > Settings > Deployment Protection >
 *                        Protection Bypass for Automation
 *
 * The doc follows Stephanie's template. Every post is one block under the
 * Heading 1 "Posts":
 *   Heading 2  day and date ("Thursday, October 22" or "Date TBD")
 *   Heading 3  what the post is about, ending in a small grey tag [wh:p05]
 *   Heading 3  CTA (Optional): ...
 *   Normal     Words: / Slide 1: ... / Link: ... / Source: / one source per line
 *   Heading 3  Visual Asset (Image Thumbnail for preview and Link to Canva Project):
 *   Normal     the visual note
 *   Heading 3  Caption/Body Copy:
 *   Normal     the caption
 * The tag maps the block to one Wormhole post. A block with no tag is a new
 * post: "Push" creates it in Wormhole and adds the tag.
 *
 * Sync = push, then pull. Push sends the fields changed in the doc since the
 * last sync. Pull rewrites the blocks Wormhole changed. If a post changed in
 * both places, the newer edit wins and Wormhole keeps the older one in its
 * version history.
 */

var POSTS_HEADING = 'Posts';
var CTA_LABEL = 'CTA (Optional):';
var VISUAL_LABEL = 'Visual Asset (Image Thumbnail for preview and Link to Canva Project):';
var CAPTION_LABEL = 'Caption/Body Copy:';
var TAG_RE = /\s*\[wh:([A-Za-z0-9_-]+)\]\s*$/;
var FIELDS = ['date', 'topic', 'cta', 'slides', 'link', 'sources', 'visual_note', 'caption'];
var MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
  'september', 'october', 'november', 'december'];

// ---------------------------------------------------------------------------
// Menu and trigger

function onOpen() {
  DocumentApp.getUi()
    .createMenu('Wormhole')
    .addItem('Sync now', 'syncNow')
    .addItem('Pull from Wormhole', 'pullFromWormhole')
    .addItem('Push to Wormhole', 'pushToWormhole')
    .addSeparator()
    .addItem('Turn on sync every 5 minutes', 'installTrigger')
    .addToUi();
}

/** Run once (menu or editor). Google asks you to approve the script then. */
function installTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'syncNow') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('syncNow').timeBased().everyMinutes(5).create();
  toast_('Wormhole sync runs every 5 minutes now.');
}

function syncNow() {
  withLock_(function () {
    var remote = fetchPosts_();
    var pushed = push_(remote);
    var pulled = pull_(remote);
    toast_('Synced. Sent ' + pushed + ', updated ' + pulled + ' in the doc.');
  });
}

function pushToWormhole() {
  withLock_(function () {
    var n = push_(fetchPosts_());
    toast_('Sent ' + n + ' post(s) to Wormhole.');
  });
}

function pullFromWormhole() {
  withLock_(function () {
    var n = pull_(fetchPosts_(), true);
    toast_('Updated ' + n + ' post(s) from Wormhole.');
  });
}

// ---------------------------------------------------------------------------
// Push and pull

/** Sends doc edits. Updates `remote` in place with what Wormhole now holds. */
function push_(remote) {
  var doc = DocumentApp.getActiveDocument();
  var editedAt = lastEdited_(doc);
  var blocks = readBlocks_(doc.getBody());
  var state = loadState_();
  var changes = [];
  var newBlocks = [];
  var seen = {};

  blocks.forEach(function (b) {
    if (b.id && seen[b.id]) return; // a copied block; the first one counts
    if (b.id) seen[b.id] = true;
    if (!b.id) {
      if (!b.fields.topic) return; // half-typed block, wait for a topic
      changes.push({ fields: toApi_(b.fields, null), edited_at: editedAt });
      newBlocks.push(b);
      return;
    }
    var r = remote[b.id];
    if (!r) return; // removed from Wormhole; leave the block alone
    var s = state[b.id];
    var changed = {};
    var any = false;
    FIELDS.forEach(function (f) {
      var mine = hash_(normField_(f, b.fields[f]));
      // Never synced: compare with Wormhole. Synced: compare with last sync.
      var before = s ? s.h[f] : hash_(normField_(f, fromApi_(r)[f]));
      if (mine !== before) { changed[f] = b.fields[f]; any = true; }
    });
    if (any) {
      changes.push({ id: b.id, fields: toApi_(changed, r), base_updated_at: s ? s.u : null, edited_at: editedAt });
    }
  });
  if (!changes.length) return 0;

  var res = call_('post', { changes: changes });
  var created = 0;
  res.results.forEach(function (x) {
    if (x.post) remote[x.post.id] = x.post;
    if (x.status === 'created') {
      var b = newBlocks[created++];
      addTag_(b.topicPara, x.post.id);
      state[x.post.id] = { u: x.post.updated_at, h: hashes_(fromApi_(x.post)) };
    }
  });
  saveState_(state);
  return changes.length;
}

/** Rewrites every block that differs from Wormhole, and adds missing posts. */
function pull_(remote, force) {
  var body = DocumentApp.getActiveDocument().getBody();
  var state = loadState_();
  var blocks = readBlocks_(body);
  var seen = {};
  var n = 0;

  // Bottom to top, so rewriting one block does not move the ones above it.
  for (var i = blocks.length - 1; i >= 0; i--) {
    var b = blocks[i];
    if (!b.id || !remote[b.id] || seen[b.id]) continue;
    seen[b.id] = true;
    var want = fromApi_(remote[b.id]);
    if (force || !sameFields_(b.fields, want)) {
      writeBlock_(body, b.start, b.end, remote[b.id]);
      n++;
    }
    state[b.id] = { u: remote[b.id].updated_at, h: hashes_(want) };
  }

  // Posts that are in Wormhole and not in the doc, in date order.
  Object.keys(remote)
    .map(function (id) { return remote[id]; })
    .filter(function (p) { return !seen[p.id]; })
    .sort(sortKey_)
    .forEach(function (p) {
      insertBlock_(body, p);
      state[p.id] = { u: p.updated_at, h: hashes_(fromApi_(p)) };
      n++;
    });

  state.__synced = new Date().toISOString();
  saveState_(state);
  return n;
}

// ---------------------------------------------------------------------------
// Reading the doc

/** The post blocks under the "Posts" heading, with their element range. */
function readBlocks_(body) {
  var paras = [];
  var inPosts = false;
  for (var i = 0; i < body.getNumChildren(); i++) {
    var el = body.getChild(i);
    if (el.getType() !== DocumentApp.ElementType.PARAGRAPH && el.getType() !== DocumentApp.ElementType.LIST_ITEM) {
      // Tables and the like stay inside the block they sit in.
      paras.push({ index: i, heading: 'OTHER', text: '', inPosts: inPosts });
      continue;
    }
    var p = el.getType() === DocumentApp.ElementType.PARAGRAPH ? el.asParagraph() : el.asListItem();
    var heading = headingName_(p.getHeading());
    if (heading === 'H1') inPosts = p.getText().trim().replace(/:$/, '') === POSTS_HEADING;
    paras.push({ index: i, heading: heading, text: p.getText(), el: p, inPosts: inPosts });
  }
  return splitBlocks(paras.filter(function (p) { return p.inPosts && p.heading !== 'H1'; }))
    .map(function (b) {
      return { id: b.id, fields: b.fields, start: b.start, end: b.end, topicPara: b.topicPara };
    });
}

function headingName_(h) {
  var H = DocumentApp.ParagraphHeading;
  if (h === H.HEADING1 || h === H.TITLE) return 'H1';
  if (h === H.HEADING2) return 'H2';
  if (h === H.HEADING3) return 'H3';
  return 'P';
}

/**
 * Pure: turns the paragraphs of the Posts section into blocks.
 * paras: [{ index, heading: 'H2'|'H3'|'P'|'OTHER', text, el }]
 */
function splitBlocks(paras) {
  var blocks = [];
  var cur = null;
  paras.forEach(function (p) {
    if (p.heading === 'H2') {
      if (cur) blocks.push(cur);
      cur = { start: p.index, end: p.index + 1, paras: [p] };
    } else if (cur) {
      cur.paras.push(p);
      cur.end = p.index + 1;
    }
  });
  if (cur) blocks.push(cur);
  return blocks.map(function (b) {
    var parsed = parseBlock(b.paras);
    parsed.start = b.start;
    parsed.end = b.end;
    return parsed;
  });
}

/** Pure: reads one block's paragraphs into Wormhole fields. */
function parseBlock(paras) {
  var f = { date: clean_(paras[0].text), topic: '', cta: '', slides: [], link: '', sources: [], visual_note: '', caption: '' };
  var id = null;
  var topicPara = null;
  var gotTopic = false;
  var sect = 'top';
  var link = [];
  var visual = [];
  var caption = [];
  for (var i = 1; i < paras.length; i++) {
    var p = paras[i];
    if (p.heading === 'OTHER') continue;
    var t = clean_(p.text);
    if (p.heading === 'H3') {
      if (startsWith_(t, CTA_LABEL)) { f.cta = t.slice(CTA_LABEL.length).trim(); sect = 'cta'; continue; }
      if (startsWith_(t, 'Visual Asset')) { sect = 'visual'; rest_(t, VISUAL_LABEL, visual); continue; }
      if (startsWith_(t, 'Caption/Body Copy')) { sect = 'caption'; rest_(t, CAPTION_LABEL, caption); continue; }
      if (sect === 'top' && !gotTopic) {
        gotTopic = true;
        var m = t.match(TAG_RE);
        if (m) id = m[1];
        f.topic = t.replace(TAG_RE, '').trim();
        topicPara = p.el || null;
        continue;
      }
    }
    if (sect === 'visual') { visual.push(t); continue; }
    if (sect === 'caption') { caption.push(t); continue; }
    if (/^Words:/i.test(t)) { sect = 'words'; var w = t.replace(/^Words:\s*/i, ''); if (w) f.slides.push(w); continue; }
    if (/^Link:/i.test(t)) { sect = 'link'; var l = t.replace(/^Link:\s*/i, ''); if (l) link.push(l); continue; }
    if (/^Sources?:/i.test(t)) { sect = 'source'; var s = t.replace(/^Sources?:\s*/i, ''); if (s) f.sources.push(s); continue; }
    if (!t) continue;
    if (sect === 'words') {
      var sm = t.match(/^(?:Slide|Frame|Card)\s*\d+\s*:\s*([\s\S]*)$/i);
      if (sm) f.slides.push(sm[1]);
      else if (f.slides.length) f.slides[f.slides.length - 1] += '\n' + t;
      else f.slides.push(t);
    } else if (sect === 'link') link.push(t);
    else if (sect === 'source') f.sources.push(t);
  }
  f.link = link.join('\n');
  f.visual_note = trimLines_(visual).join('\n');
  f.caption = trimLines_(caption).join('\n');
  return { id: id, fields: f, topicPara: topicPara };
}

// ---------------------------------------------------------------------------
// Writing the doc

/** Pure: the paragraphs that make up one post block. */
function renderBlock(post) {
  var out = [];
  out.push({ heading: 'H2', text: post.date_tbd ? 'Date TBD' : dayLabel(post.iso_date) });
  out.push({ heading: 'H3', text: post.topic || 'Untitled post', tag: post.id });
  out.push({ heading: 'H3', text: CTA_LABEL + (post.cta ? ' ' + post.cta : '') });
  out.push({ heading: 'P', text: 'Words:' });
  (post.slides || []).forEach(function (s, i) {
    String(s).split('\n').forEach(function (line, j) {
      out.push({ heading: 'P', text: j === 0 ? 'Slide ' + (i + 1) + ': ' + line : line });
    });
  });
  String(post.link || '').split('\n').forEach(function (line, j) {
    out.push({ heading: 'P', text: j === 0 ? 'Link:' + (line ? ' ' + line : '') : line });
  });
  out.push({ heading: 'P', text: 'Source:' });
  (post.sources || []).forEach(function (s) { if (String(s).trim()) out.push({ heading: 'P', text: s }); });
  out.push({ heading: 'H3', text: VISUAL_LABEL });
  splitLines_(post.visual_note).forEach(function (line) { out.push({ heading: 'P', text: line }); });
  out.push({ heading: 'H3', text: CAPTION_LABEL });
  splitLines_(post.caption).forEach(function (line) { out.push({ heading: 'P', text: line }); });
  return out;
}

function writeBlock_(body, start, end, post) {
  // A doc must keep a paragraph after the last block, or the last element
  // cannot be removed.
  if (end >= body.getNumChildren()) body.appendParagraph('');
  for (var i = end - 1; i >= start; i--) body.removeChild(body.getChild(i));
  insertAt_(body, start, renderBlock(post));
}

function insertBlock_(body, post) {
  var blocks = readBlocks_(body);
  var at = null;
  for (var i = 0; i < blocks.length; i++) {
    var other = blocks[i];
    var key = other.fields.date === 'Date TBD' ? '9' : isoFromLabel(other.fields.date, post.iso_date) || '';
    if (key && key > sortValue_(post)) { at = other.start; break; }
  }
  if (at === null) {
    // After the last block, or at the end of the Posts section.
    at = blocks.length ? blocks[blocks.length - 1].end : postsEnd_(body);
  }
  if (at >= body.getNumChildren()) body.appendParagraph('');
  insertAt_(body, at, renderBlock(post));
}

function postsEnd_(body) {
  var inPosts = false;
  for (var i = 0; i < body.getNumChildren(); i++) {
    var el = body.getChild(i);
    if (el.getType() !== DocumentApp.ElementType.PARAGRAPH) continue;
    var p = el.asParagraph();
    if (headingName_(p.getHeading()) !== 'H1') continue;
    if (inPosts) return i;
    inPosts = p.getText().trim().replace(/:$/, '') === POSTS_HEADING;
  }
  if (!inPosts) body.appendParagraph(POSTS_HEADING).setHeading(DocumentApp.ParagraphHeading.HEADING1);
  return body.getNumChildren();
}

function insertAt_(body, index, paras) {
  var H = DocumentApp.ParagraphHeading;
  paras.forEach(function (x, k) {
    var p = body.insertParagraph(index + k, x.text);
    p.setHeading(x.heading === 'H2' ? H.HEADING2 : x.heading === 'H3' ? H.HEADING3 : H.NORMAL);
    var text = p.editAsText();
    if (x.text) text.setLinkUrl(0, x.text.length - 1, null);
    linkify_(text, x.text);
    if (x.tag) addTag_(p, x.tag);
  });
}

function addTag_(para, id) {
  if (!para) return;
  var text = para.editAsText();
  var from = text.getText().length;
  text.appendText(' [wh:' + id + ']');
  var to = text.getText().length - 1;
  text.setFontSize(from, to, 8).setForegroundColor(from, to, '#999999').setLinkUrl(from, to, null);
}

function linkify_(text, s) {
  var re = /https?:\/\/[^\s<>()]+[^\s<>().,;:!?'"]/g;
  var m;
  while ((m = re.exec(s))) text.setLinkUrl(m.index, m.index + m[0].length - 1, m[0]);
}

// ---------------------------------------------------------------------------
// Fields, dates, comparison (pure)

/** Wormhole's API post -> the doc's field shape. */
function fromApi_(p) {
  return {
    date: p.date_tbd ? 'Date TBD' : dayLabel(p.iso_date),
    topic: p.topic || '',
    cta: p.cta || '',
    slides: p.slides || [],
    link: p.link || '',
    sources: p.sources || [],
    visual_note: p.visual_note || '',
    caption: p.caption || '',
  };
}

/** The doc's fields -> what POST /api/wormhole/sync takes. */
function toApi_(fields, current) {
  var out = {};
  Object.keys(fields).forEach(function (k) {
    if (k !== 'date') { out[k] = fields[k]; return; }
    if (/^date tbd$/i.test(String(fields.date).trim())) { out.date_tbd = true; return; }
    var iso = isoFromLabel(fields.date, current ? current.iso_date : null);
    if (iso) { out.iso_date = iso; out.date_tbd = false; }
  });
  return out;
}

function dayLabel(iso) {
  var d = new Date(iso + 'T12:00:00Z');
  var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var month = MONTHS[d.getUTCMonth()];
  return days[d.getUTCDay()] + ', ' + month.charAt(0).toUpperCase() + month.slice(1) + ' ' + d.getUTCDate();
}

/**
 * "Thursday, October 22" -> "2026-10-22". The weekday is ignored. The year
 * comes from the post's current date, or from today, picking the nearest.
 */
function isoFromLabel(label, nearIso) {
  var m = String(label || '').toLowerCase().match(/([a-z]+)\.?\s+(\d{1,2})(?:st|nd|rd|th)?\b/g);
  if (!m) return null;
  for (var k = 0; k < m.length; k++) {
    var parts = m[k].match(/([a-z]+)\.?\s+(\d{1,2})/);
    var mi = -1;
    for (var j = 0; j < MONTHS.length; j++) {
      if (MONTHS[j] === parts[1] || MONTHS[j].slice(0, 3) === parts[1].slice(0, 3) && parts[1].length >= 3) { mi = j; break; }
    }
    if (mi < 0) continue;
    var day = Number(parts[2]);
    if (day < 1 || day > 31) continue;
    var near = nearIso ? new Date(nearIso + 'T12:00:00Z') : new Date();
    var best = null;
    [-1, 0, 1].forEach(function (dy) {
      var c = new Date(Date.UTC(near.getUTCFullYear() + dy, mi, day, 12));
      if (c.getUTCMonth() !== mi) return;
      if (!best || Math.abs(c - near) < Math.abs(best - near)) best = c;
    });
    if (best) return best.toISOString().slice(0, 10);
  }
  return null;
}

function normField_(f, v) {
  if (f === 'slides' || f === 'sources') {
    return (v || []).map(function (x) { return trimLines_(String(x).split('\n')).filter(Boolean).join('\n'); })
      .filter(Boolean).join('\n\u0001');
  }
  return trimLines_(String(v || '').split('\n')).filter(Boolean).join('\n');
}

function sameFields_(a, b) {
  for (var i = 0; i < FIELDS.length; i++) {
    if (normField_(FIELDS[i], a[FIELDS[i]]) !== normField_(FIELDS[i], b[FIELDS[i]])) return false;
  }
  return true;
}

function hashes_(fields) {
  var h = {};
  FIELDS.forEach(function (f) { h[f] = hash_(normField_(f, fields[f])); });
  return h;
}

function hash_(s) {
  var bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, s, Utilities.Charset.UTF_8);
  return Utilities.base64Encode(bytes);
}

function sortValue_(p) { return p.date_tbd ? '9' : p.iso_date; }
function sortKey_(a, b) { return sortValue_(a) < sortValue_(b) ? -1 : sortValue_(a) > sortValue_(b) ? 1 : (a.id < b.id ? -1 : 1); }

function clean_(s) { return String(s || '').replace(/[\r\u000b]/g, '\n').replace(/ /g, ' ').trim(); }
function startsWith_(s, prefix) { return s.toLowerCase().indexOf(prefix.toLowerCase().replace(/:$/, '')) === 0; }
function rest_(t, label, into) { var r = t.slice(label.length).trim(); if (t.length > label.length && r) into.push(r); }
function splitLines_(s) { return String(s || '').split('\n'); }

/** Trims each line and drops empty lines at the start and end. */
function trimLines_(lines) {
  var out = lines.map(function (l) { return String(l).trim(); });
  while (out.length && !out[0]) out.shift();
  while (out.length && !out[out.length - 1]) out.pop();
  return out;
}

// ---------------------------------------------------------------------------
// Wormhole API, state, lock

/**
 * When the doc was last edited. Never earlier than the edit we are sending,
 * so the doc does not lose a tie it should win. Falls back to now.
 */
function lastEdited_(doc) {
  try {
    return DriveApp.getFileById(doc.getId()).getLastUpdated().toISOString();
  } catch (e) {
    return new Date().toISOString();
  }
}

function config_() {
  var props = PropertiesService.getScriptProperties();
  var url = (props.getProperty('WORMHOLE_URL') || '').replace(/\/+$/, '');
  var token = props.getProperty('WORMHOLE_SYNC_TOKEN') || '';
  if (!url || !token) throw new Error('Set WORMHOLE_URL and WORMHOLE_SYNC_TOKEN in Project Settings > Script Properties.');
  return { url: url, token: token, bypass: props.getProperty('VERCEL_BYPASS') || '' };
}

function call_(method, payload) {
  var c = config_();
  var res = UrlFetchApp.fetch(c.url + '/api/wormhole/sync', {
    method: method,
    contentType: 'application/json',
    headers: c.bypass
      ? { Authorization: 'Bearer ' + c.token, 'x-vercel-protection-bypass': c.bypass }
      : { Authorization: 'Bearer ' + c.token },
    payload: payload ? JSON.stringify(payload) : undefined,
    muteHttpExceptions: true,
  });
  if (res.getResponseCode() !== 200) {
    throw new Error('Wormhole said ' + res.getResponseCode() + ': ' + res.getContentText().slice(0, 200));
  }
  return JSON.parse(res.getContentText());
}

function fetchPosts_() {
  var map = {};
  call_('get').posts.forEach(function (p) { map[p.id] = p; });
  return map;
}

// One property per post: { u: Wormhole updated_at at last sync, h: field hashes }.
function loadState_() {
  var all = PropertiesService.getDocumentProperties().getProperties();
  var state = {};
  Object.keys(all).forEach(function (k) {
    if (k.indexOf('wh:') === 0) state[k.slice(3)] = JSON.parse(all[k]);
    if (k === 'synced') state.__synced = all[k];
  });
  return state;
}

function saveState_(state) {
  var out = {};
  Object.keys(state).forEach(function (k) {
    if (k === '__synced') out.synced = state[k];
    else out['wh:' + k] = JSON.stringify(state[k]);
  });
  PropertiesService.getDocumentProperties().setProperties(out);
}

function withLock_(fn) {
  var lock = LockService.getDocumentLock();
  if (!lock.tryLock(30000)) return;
  try { fn(); } finally { lock.releaseLock(); }
}

function toast_(msg) {
  try { DocumentApp.getUi().alert(msg); } catch (e) { Logger.log(msg); } // no UI when the timer runs it
}

// Lets the parsing be tested outside Google (node, see Code.test.ts).
if (typeof module !== 'undefined') {
  module.exports = { parseBlock: parseBlock, splitBlocks: splitBlocks, renderBlock: renderBlock, dayLabel: dayLabel, isoFromLabel: isoFromLabel, toApi_: toApi_, fromApi_: fromApi_, normField_: normField_, sameFields_: sameFields_ };
}
