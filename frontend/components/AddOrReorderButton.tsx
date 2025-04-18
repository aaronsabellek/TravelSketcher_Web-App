import { motion, AnimatePresence } from "framer-motion";

interface Props {
  isReorderMode: boolean;
  hasOrderChanged: boolean;
  saveNewOrder: () => void;
  handleAddClick: () => void;
}

const AddOrReorderButton: React.FC<Props> = ({
  isReorderMode,
  hasOrderChanged,
  saveNewOrder,
  handleAddClick
}) => {
  return (
    <AnimatePresence mode="wait">
      {isReorderMode ? (
        <motion.div
          key="save-button"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          transition={{ duration: 0.3 }}
          className="flex justify-center mt-6"
        >
          <button
            onClick={saveNewOrder}
            disabled={!hasOrderChanged}
            className={`px-4 py-2 font-light bg-blue-500 rounded text-white rounded-xl transition ${
              hasOrderChanged
                ? 'opacity-100 hover:bg-blue-600 cursor-pointer'
                : 'opacity-50'
            }`}
          >
            💾 Save
          </button>
        </motion.div>
      ) : (
        <motion.div
          key="add-button"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 0.3, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          transition={{ duration: 0.3 }}
          className="flex justify-center mt-4"
        >
          <button
            onClick={handleAddClick}
            className="transition-opacity opacity-70 hover:opacity-100 hover:scale-115 duration-300 cursor-pointer"
          >
            <img src="/plus_icon.png" alt="Add Destination" className="w-12 h-12" />
          </button>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default AddOrReorderButton;