import { useState } from 'react';
import { toast } from 'sonner';

import { validatePasswordRules, validatePasswordMatch } from '@/utils/validation';

interface UsePasswordValidationProps {
  initialPassword1?: string;
  initialPassword2?: string;
}

export const usePasswordValidation = ({ initialPassword1 = '', initialPassword2 = '' }: UsePasswordValidationProps) => {

  const [password1, setPassword1] = useState(initialPassword1);
  const [password2, setPassword2] = useState(initialPassword2);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  // Set errors
  const ruleError = validatePasswordRules(password1);
  const matchError = validatePasswordMatch(password1, password2);

  // Set conditions for inputs
  const isDisabled =
    saving ||
    password1.trim() === '' ||
    password2.trim() === '' ||
    ruleError !== null ||
    matchError !== null;

  // Submit handler
  const handleSubmit = async (e: React.FormEvent, onSubmit: (password1: string, password2: string) => Promise<void>) => {

    e.preventDefault();
    setSaving(true);

    // Clear previous errors
    if (ruleError || matchError) {
      setSaving(false);
      if (ruleError) toast.error(ruleError);
      if (matchError) toast.error(matchError);
      return;
    }

    try {
      await onSubmit(password1, password2);
      toast.success('Password changed successfully!');
    } catch (err: any) {
      toast.error(err.message || 'An unexpected error occurred.');
      setSaving(false);
    }
  };

  return {
    password1,
    password2,
    setPassword1,
    setPassword2,
    ruleError,
    matchError,
    isDisabled,
    saving,
    error,
    handleSubmit,
  };
};