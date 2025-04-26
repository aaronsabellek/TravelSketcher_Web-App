import React from "react";

interface SectionProps {
  title: string;
  children: React.ReactNode;
}

export default function Section({ title, children }: SectionProps) {
  return (
    <section className="mb-8">
      <h2 className="text-2xl font-semibold mb-4 grey">{title}</h2>
      <div className="text-base space-y-2">{children}</div>
    </section>
  );
}