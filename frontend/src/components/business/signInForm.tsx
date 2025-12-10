"use client";

import React, { useState } from 'react';
import Input from "@/components/ui/input"
import PasswordField from '@/components/ui/passwordField';
import Button from '@/components/ui/button';
import Form from '@/components/ui/form';
import { useRouter } from 'next/navigation';
import { signIn } from '@/lib/auth';

export const SignInForm: React.FC = () => {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await signIn(email, password);
      router.push('/Dashboard');
    } catch (err) {
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: '0 auto', padding: 24 }}>
      <h2>Sign In</h2>
      {error && <div style={{ color: 'red', marginBottom: 12 }}>{error}</div>}

      <Input
        label="Email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />

      <PasswordField
        label="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />

      <Button
        variant="primary"
        type="submit"
        disabled={loading || !email || !password}
      >
        {loading ? 'Signing in...' : 'Sign In'}
      </Button>
    </Form>
  );
};

export default SignInForm;

