import copy, sys
from pptx import Presentation
def copy_slide(src_slide, dst):
    s = dst.slides.add_slide(dst.slide_layouts[6])
    for shp in list(s.shapes): shp._element.getparent().remove(shp._element)
    # background
    bg = src_slide._element.cSld.bg
    if bg is not None:
        s._element.cSld.insert(0, copy.deepcopy(bg))
    rid_map = {}
    for rel in src_slide.part.rels.values():
        if 'image' in rel.reltype:
            rid_map[rel.rId] = s.part.relate_to(rel._target, rel.reltype)
    for el in src_slide.shapes._spTree.iterchildren():
        if el.tag.endswith('}nvGrpSpPr') or el.tag.endswith('}grpSpPr'): continue
        new = copy.deepcopy(el)
        for node in new.iter():
            for k, v in list(node.attrib.items()):
                if k.endswith('}embed') and v in rid_map: node.set(k, rid_map[v])
        s.shapes._spTree.append(new)
her = Presentation(sys.argv[1]); mine = Presentation(sys.argv[2])
while len(her.slides) > 2:
    sid = her.slides._sldIdLst[-1]; her.part.drop_rel(sid.rId); her.slides._sldIdLst.remove(sid)
for sl in list(mine.slides)[2:]: copy_slide(sl, her)
her.save(sys.argv[3])
print(len(her.slides), her.slide_width, mine.slide_width)
