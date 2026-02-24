export const CATEGORY_TO_DEPARTMENT: Record<string, string> = {
  clinica: 'Clínica Médica',
  gineco: 'Ginecología',
  pediatria: 'Pediatría',
  urologia: 'Urología',
  traumatologia: 'Traumatología'
};

export function resolveDepartmentName(category: string) {
  return CATEGORY_TO_DEPARTMENT[category] ?? 'Clínica Médica';
}

export function llmRoutingHookDisabled() {
  return { enabled: false, reason: 'MVP con reglas simples categoría → departamento' };
}
