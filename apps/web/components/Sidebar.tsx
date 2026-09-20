'use client';

import { SECTION_LABELS, type SmartFolder } from '@/lib/types';

/**
 * Smart folders, grouped Workshops / Asset types / Views / Saved.
 *
 * They are saved filters, not containers: clicking one replaces the current
 * filters, and one asset shows up in every folder it matches.
 */
export function Sidebar({
  folders,
  activeId,
  onPick,
  onSaveCurrent,
}: {
  folders: SmartFolder[];
  activeId: number | null;
  onPick: (folder: SmartFolder | null) => void;
  onSaveCurrent: () => void;
}) {
  const sections: SmartFolder['section'][] = ['workshops', 'asset_types', 'views', 'saved'];

  return (
    <aside className="w-56 shrink-0 border-r border-green-mid/20 p-3 text-sm">
      <button
        onClick={() => onPick(null)}
        className={`mb-3 w-full rounded px-2 py-1 text-left ${
          activeId === null ? 'bg-green-deep text-cream' : 'hover:bg-green-bright/15'
        }`}
      >
        Everything
      </button>

      {sections.map((section) => {
        const inSection = folders.filter((f) => f.section === section);
        if (inSection.length === 0) return null;

        return (
          <div key={section} className="mb-4">
            <h3 className="mb-1 text-xs font-semibold uppercase tracking-wide text-green-mid">
              {SECTION_LABELS[section]}
            </h3>
            <ul className="space-y-0.5">
              {inSection.map((folder) => (
                <li key={folder.id}>
                  <button
                    onClick={() => onPick(folder)}
                    className={`w-full truncate rounded px-2 py-1 text-left ${
                      activeId === folder.id
                        ? 'bg-green-deep text-cream'
                        : 'hover:bg-green-bright/15'
                    }`}
                    title={folder.name}
                  >
                    {folder.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        );
      })}

      <button
        onClick={onSaveCurrent}
        className="mt-2 w-full rounded border border-green-mid/40 px-2 py-1 text-xs hover:bg-green-bright/10"
      >
        Save current filters as folder
      </button>
    </aside>
  );
}
