import React from "react";

import Section from "@/components/Section";

export default function PrivacyPolicyPage() {
  return (
    <main className="max-w-3xl mx-auto p-8 text-gray-700">
      <h1 className="text-3xl font-bold mb-6">Privacy Policy</h1>
      <p className="text-sm text-gray-500 mb-10">Last updated: April 26, 2025</p>

      <Section title="Information We Collect">
        <ul className="list-disc list-inside space-y-2">
          <li>Username</li>
          <li>Email address</li>
          <li>Password (securely encrypted)</li>
          <li>City</li>
          <li>Country (optional)</li>
          <li>Your saved destinations and activities</li>
        </ul>
      </Section>

      <Section title="How We Use Your Data">
        <ul className="list-disc list-inside space-y-2">
          <li>Provide and maintain your TravelSketcher account</li>
          <li>Allow you to manage your destinations and activities</li>
          <li>Manage user sessions and improve error handling through cookies and logs</li>
          <li>We do not use your data for advertising or analytics purposes</li>
        </ul>
      </Section>

      <Section title="Data Storage">
        <ul className="list-disc list-inside space-y-2">
          <li>Your data is stored securely with our hosting providers</li>
          <li>We retain your information as long as your account is active</li>
          <li>Deleting your account permanently removes your data</li>
          <li>International data transfers may occur depending on hosting location</li>
        </ul>
      </Section>

      <Section title="Third Parties">
        <ul className="list-disc list-inside space-y-2">
          <li>We integrate Unsplash to display high-quality images</li>
          <li>We do not share your personal data with Unsplash or others</li>
        </ul>
      </Section>

      <Section title="Cookies">
        <ul className="list-disc list-inside space-y-2">
          <li>We use cookies only for session management and error logging</li>
          <li>No tracking or advertising cookies are used</li>
        </ul>
      </Section>

      <Section title="Your Rights">
        <ul className="list-disc list-inside space-y-2">
          <li>Access, correct, or request deletion of your data at any time</li>
          <li>Contact: support@travelsketcher.com</li>
        </ul>
      </Section>
    </main>
  );
}