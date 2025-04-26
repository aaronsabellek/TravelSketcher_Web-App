import React from "react";

import Section from "@/components/Section";

export default function TermsAndConditionsPage() {
  return (
    <main className="max-w-3xl mx-auto p-8 text-gray-700">
      <h1 className="text-3xl font-bold mb-6">Terms and Conditions</h1>
      <p className="text-sm text-gray-500 mb-10">Last updated: April 26, 2025</p>

      <Section title="Account Registration">
        <ul className="list-disc list-inside space-y-2">
          <li>You must be at least 13 years old to create an account</li>
          <li>All information provided must be accurate</li>
        </ul>
      </Section>

      <Section title="User Content">
        <ul className="list-disc list-inside space-y-2">
          <li>TravelSketcher allows you to save private travel information</li>
          <li>Content you save is not visible to other users</li>
          <li>Using the service unlawfully or attempting to overload it is prohibited</li>
          <li>We reserve the right to suspend accounts violating these terms</li>
        </ul>
      </Section>

      <Section title="Service Availability">
        <ul className="list-disc list-inside space-y-2">
          <li>TravelSketcher is offered free of charge and without ads</li>
          <li>We do not guarantee uninterrupted service</li>
        </ul>
      </Section>

      <Section title="Desclaimer">
        <ul className="list-disc list-inside space-y-2">
          <li>The service is provided "as is"</li>
          <li>We are not responsible for any data loss or damages</li>
        </ul>
      </Section>

      <Section title="Changes to These Terms">
        <ul className="list-disc list-inside space-y-2">
          <li>Terms may be updated from time to time</li>
          <li>We will notify users of significant changes</li>
        </ul>
      </Section>
    </main>
  );
}