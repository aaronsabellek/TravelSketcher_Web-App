import React from 'react';

import { Block } from '@/types/models'

// Text section for footer pages
export default function Section({ title, children }: Block) {
  return (
    <section className="mb-8">
      <h2 className="text-2xl font-semibold mb-4 grey">{title}</h2>
      <div className="text-base space-y-2">{children}</div>
    </section>
  );
}