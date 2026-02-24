export const env = {
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL ?? '',
  supabaseAnonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? '',
  supabaseServiceRole: process.env.SUPABASE_SERVICE_ROLE_KEY ?? ''
};

export function assertEnv() {
  if (!env.supabaseUrl || !env.supabaseAnonKey) {
    throw new Error('Faltan NEXT_PUBLIC_SUPABASE_URL o NEXT_PUBLIC_SUPABASE_ANON_KEY');
  }
}
