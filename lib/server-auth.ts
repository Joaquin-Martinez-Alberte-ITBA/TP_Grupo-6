import { createClient } from '@supabase/supabase-js';
import { env } from './env';

export function getUserClient(authHeader?: string | null) {
  if (!authHeader) return null;
  return createClient(env.supabaseUrl, env.supabaseAnonKey, {
    global: { headers: { Authorization: authHeader } },
    auth: { persistSession: false, autoRefreshToken: false }
  });
}
