import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

import { Destination, Activity } from '../../types/models';

interface Props<T> {
  data: T;
  type: 'destination' | 'activity';
  isExpanded: boolean;
  onExpand: () => void;
  onCollapse: () => void;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  onNote: (id: string) => void;
  menuOpenFor: string | null;
  setMenuOpenFor: (id: string | null) => void;
  menuRef: React.RefObject<HTMLDivElement | null>;
  default_img?: string;
  isReorderMode: boolean;
  index: number;
  moveDestinationUp: (index: number) => void;
  moveDestinationDown: (index: number) => void;
  items: T[];
  setExpandedCard: (id: string | null) => void;
  onLinkClick?: (id: string, web_link?: string) => void;
  userCity?: string | null;
}

const DestinationCard = <T extends Destination | Activity>({
  data,
  type,
  isExpanded,
  onEdit,
  onDelete,
  onNote,
  menuOpenFor,
  setMenuOpenFor,
  menuRef,
  default_img = 'https://images.unsplash.com/photo-1486184885347-1464b5f10296?q=80&w=1168&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
  isReorderMode,
  index,
  moveDestinationUp,
  moveDestinationDown,
  onLinkClick,
  items,
  setExpandedCard,
  userCity
}: Props<T>) => {
  return (
    <motion.div
      key={data.id}
      layout="position"
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="relative flex flex-col items-center space-y-2"
    >
      {/* Reorder buttons */}
      <AnimatePresence>
        {isReorderMode && (
          <motion.div
            key={`reorder-buttons-${data.id}`}
            layout
            layoutId={`reorder-${data.id}`}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.5 }}
            className="absolute -top-4 z-30 flex space-x-4"
            data-ignore-click
          >
            <button
              onClick={() => moveDestinationUp(index)}
              disabled={index === 0}
              className="transition-transform duration-200 hover:scale-125"
            >
              <img src="/left_icon.png" className="h-3" />
            </button>
            <button
              onClick={() => moveDestinationDown(index)}
              disabled={index === items.length - 1}
              className="transition-transform duration-200 hover:scale-125"
            >
              <img src="/right_icon.png" className="h-3" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Destination container */}
      <div
        className="w-full mt-3 bg-white hover:brightness-95 rounded-t-lg pb-2"
        onClick={(e) => {
          const target = e.target as HTMLElement;
          if (target.closest('[data-ignore-click]')) return; // Events ignorieren
          setExpandedCard(isExpanded ? null : data.id);
        }}
      >
        {/* Image */}
        <div className="relative aspect-[16/12] w-full rounded-t-lg overflow-hidden">
          <a
            href={type === 'destination' ? `/activity/get_all/${data.id}` : (data as Activity).web_link || '#'}
            target={type === 'activity' ? "_blank" : ''}
            rel={type === 'activity' ? 'noopener noreferrer' : ''}
            className={type === 'activity' && !(data as Activity).web_link ? 'pointer-events-none cursor-not-allowed' : ''}
          >
            <img
              src={data.img_link || default_img}
              alt={data.title}
              className="w-full h-full object-cover hover:scale-105 transition-all duration-500"
              onError={(e) => {
                (e.currentTarget as HTMLImageElement).src = default_img;
              }}
            />
          </a>

          {/* Edit/Delete Menu */}
          <div className="absolute top-2 right-2 text-white">
            <button
              onClick={(e) => {
                e.stopPropagation(); // verhindert, dass das Card-Click-Event ausgelöst wird
                setMenuOpenFor(data.id === menuOpenFor ? null : data.id);
              }}
              className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-500/10 hover:bg-gray-500/20 transition-transform duration-200 hover:scale-110 cursor-pointer"
            >
              ⋮
            </button>

            {menuOpenFor === data.id && (
              <div
                ref={menuRef}
                className="absolute right-0 mt-2 w-28 bg-white text-black rounded shadow-md z-50"
                onClick={(e) => e.stopPropagation()} // damit der Card-Click nicht ausgelöst wird
              >
                <button
                  onClick={() => onEdit(data.id)}
                  className="block w-full text-left px-4 py-2 hover:bg-gray-100 cursor-pointer"
                >
                  ✏️ Edit
                </button>
                <button
                  onClick={() => onDelete(data.id)}
                  className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-red-600 cursor-pointer"
                >
                  🗑️ Delete
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Title */}
        <div>
          <div className="flex p-2">
            <div className="mr-5">
              <a
                href={type === 'destination' ? `/activity/get_all/${data.id}` : (data as Activity).web_link || '#'}
                target={type === 'activity' ? "_blank" : ''}
                rel={type === 'activity' ? 'noopener noreferrer' : ''}
                className={type === 'activity' && !(data as Activity).web_link ? 'pointer-events-none cursor-not-allowed' : ''}
              >
                <h2 className="text-xl font-semibold hover:underline">{data.title}</h2>
              </a>
              {type === 'destination' && (
                <p className="text-sm text-gray-500">{(data as Destination).country}</p>
              )}
            </div>
          </div>

          {/* Tags */}
          {data.tags && data.tags.trim() !== '' && (
            <motion.div
              layout
              initial={false}
              animate={{ opacity: 1 }}
              transition={{ layout: { duration: 0.4, ease: 'easeInOut' } }}
              className="px-2 mt-2"
            >
              <div
                className={isExpanded ? 'flex flex-wrap gap-2' : 'whitespace-nowrap overflow-x-auto pb-2'}
              >
                {data.tags.split(',').map((tag, idx) => (
                  <motion.span
                    layout
                    key={idx}
                    className="text-xs bg-gray-200 rounded-full px-2 py-1 mr-2 mb-1 inline-block"
                  >
                    {tag.trim()}
                  </motion.span>
                ))}
              </div>
            </motion.div>
          )}

          {/* Link icons */}
          <div className="flex justify-between space-x-4 p-2">
            <div className="grid grid-cols-3 gap-3">

              {type === 'destination' && userCity ? (
                <button
                  onClick={() =>
                    window.open(`https://www.rome2rio.com/map/${userCity}/${data.title}`, '_blank')
                  }
                  className="text-blue-500 hover:text-blue-700 cursor-pointer"
                >
                  <img src="/rome2rio_icon.png" className="h-7 hover:scale-115" />
                </button>
              ) : type === 'activity' ? (
                <button
                  onClick={() => onLinkClick?.(data.id, (data as any).web_link)}
                  className={`cursor-pointer ${(data as any).web_link ? 'text-blue-500' : 'text-gray-400'}`}
                >
                  <img
                    src="/link_icon.png"
                    className={`h-6 hover:scale-110 ${(data as any).web_link ? '' : 'opacity-50'}`}
                  />
                </button>
              ) : null}

              {type === 'destination' && (
              <button
                onClick={() =>
                  window.open(`https://www.booking.com/${data.title}`, '_blank')
                }
                className="text-blue-500 relative right-2 hover:text-blue-700 cursor-pointer"
              >
                <img src="/booking_icon.png" className="h-7 hover:scale-115" />
              </button>
              )}

              <button
                onClick={() =>
                  {type === 'destination' ? (
                    window.open(`https://www.google.com/search?q=${data.title} ${(data as Destination).country}`, '_blank')
                  ) : (
                    window.open(`https://www.google.com/search?q=${data.title}`, '_blank')
                  )}
                }
                className="text-blue-500 relative right-2 hover:text-blue-700 cursor-pointer"
              >
                <img src="/google_icon.png" className="h-7 hover:scale-115" />
              </button>
            </div>

            {/* Notes icon */}
            <div>
              <button
                data-ignore-click
                onClick={(e) => {
                  e.stopPropagation();
                  onNote(data.id);
                }}
                className="text-green-500 h-7 hover:text-green-700 justify-end"
              >
                <img src="/notes_icon.png" alt="Notizen" className="h-7 hover:scale-115 cursor-pointer" />
              </button>
            </div>

          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default DestinationCard;