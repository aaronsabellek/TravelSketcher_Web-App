import React from 'react';

interface TagsInputProps {
  tagInput: string;
  setTagInput: (val: string) => void;
  tagsArray: string[];
  setTagsArray: (val: string[]) => void;
  onRemoveTag: (tag: string) => void;
}

// Administers tag usage
const TagsInput: React.FC<TagsInputProps> = ({
  tagInput,
  setTagInput,
  tagsArray,
  setTagsArray,
  onRemoveTag,
}) => {
  const handleTagKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === ',' || e.key === 'Enter') {
      e.preventDefault();
      const newTag = tagInput.trim().replace(/,$/, '');
      if (newTag && !tagsArray.includes(newTag)) {
        setTagsArray([...tagsArray, newTag]);
      }
      setTagInput('');
    }
  };

  return (
    <div className="mb-4">
      <label htmlFor="tags" className="block text-sm font-medium text-gray-700">
        Tags
      </label>
      <input
        type="text"
        id="tags"
        value={tagInput}
        onChange={(e) => setTagInput(e.target.value)}
        onKeyDown={handleTagKeyDown}
        placeholder="Separate with commas"
        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white"
      />
      <div className="mt-2 flex flex-wrap">
        {tagsArray.map((tag) => (
          <span
            key={tag}
            className="text-xs bg-gray-200 rounded-full px-2 py-1 mr-2 mb-1 inline-flex items-center"
          >
            {tag}
            <button
              type="button"
              onClick={() => onRemoveTag(tag)}
              className="ml-1 text-gray-500 hover:text-red-500"
            >
              &times;
            </button>
          </span>
        ))}
      </div>
    </div>
  );
};

export default TagsInput;
