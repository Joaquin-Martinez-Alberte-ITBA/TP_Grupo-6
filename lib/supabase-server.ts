import { createClient } from '@supabase/supabase-js';
import { env } from './env';

export function getServiceSupabase() {
  if (!env.supabaseServiceRole) throw new Error('Falta SUPABASE_SERVICE_ROLE_KEY');
  return createClient(env.supabaseUrl, env.supabaseServiceRole, {
    auth: { autoRefreshToken: false, persistSession: false }
  });
}

export function getAnonSupabase() {
  return createClient(env.supabaseUrl, env.supabaseAnonKey, {
    auth: { autoRefreshToken: false, persistSession: false }
  });
}
