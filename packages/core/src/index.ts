export type Phase =
  | "foundation"
  | "novice"
  | "adept"
  | "kanji"
  | "workplace"
  | "career";

export type QuestType = "lesson" | "checkpoint" | "final_exam";

export interface QuestDefinition {
  day: number;
  type: QuestType;
}

export interface BadgeDefinition {
  id: string;
  unlockDay: number;
  requires: readonly number[];
}

export interface ProgressState {
  version: 1;
  completedQuests: number[];
  xp: number;
  badges: string[];
  currentDay: number;
  currentPhase: Phase;
}

export interface ProgressConfig {
  quests: readonly QuestDefinition[];
  badges: readonly BadgeDefinition[];
}

const XP: Record<QuestType, number> = {
  lesson: 100,
  checkpoint: 250,
  final_exam: 500,
};

const PHASES: readonly [Phase, number, number][] = [
  ["foundation", 1, 5],
  ["novice", 6, 10],
  ["adept", 11, 15],
  ["kanji", 16, 20],
  ["workplace", 21, 25],
  ["career", 26, 30],
];

function phaseForDay(day: number): Phase {
  const phase = PHASES.find(([, start, end]) => day >= start && day <= end);
  if (!phase) throw new Error(`invalid day: ${day}`);
  return phase[0];
}

function validateDays(days: readonly number[]): void {
  for (const day of days) {
    if (!Number.isInteger(day) || day < 1 || day > 30) {
      throw new Error("days must be integers between 1 and 30");
    }
  }
}

export function calculateXp(completedQuests: readonly number[], quests: readonly QuestDefinition[]): number {
  validateDays(completedQuests);
  const byDay = new Map(quests.map((quest) => [quest.day, quest]));
  return [...new Set(completedQuests)].reduce((total, day) => {
    const quest = byDay.get(day);
    if (!quest) throw new Error(`missing quest definition for day-${String(day).padStart(2, "0")}`);
    return total + XP[quest.type];
  }, 0);
}

export function getUnlockedBadges(
  completedQuests: readonly number[],
  badges: readonly BadgeDefinition[],
): string[] {
  const completed = new Set(completedQuests);
  return badges
    .filter((badge) => completed.has(badge.unlockDay) && badge.requires.every((day) => completed.has(day)))
    .map((badge) => badge.id)
    .sort();
}

export function resolveProgress(
  completedQuests: readonly number[],
  config: ProgressConfig,
): ProgressState {
  validateDays(completedQuests);
  const completed = [...new Set(completedQuests)].sort((a, b) => a - b);
  const xp = calculateXp(completed, config.quests);
  const badges = getUnlockedBadges(completed, config.badges);
  const currentDay = completed.length === 30
    ? 30
    : Array.from({ length: 30 }, (_, index) => index + 1).find((day) => !completed.includes(day)) ?? 30;

  return {
    version: 1,
    completedQuests: completed,
    xp,
    badges,
    currentDay,
    currentPhase: phaseForDay(currentDay),
  };
}

export function canCompleteQuest(day: number, completedQuests: readonly number[]): boolean {
  validateDays([day]);
  if (day === 1) return true;
  return completedQuests.includes(day - 1);
}

export function completeQuest(day: number, completedQuests: readonly number[]): number[] {
  validateDays([day]);
  if (!canCompleteQuest(day, completedQuests)) {
    throw new Error(`day-${String(day).padStart(2, "0")} requires day-${String(day - 1).padStart(2, "0")}`);
  }
  return [...new Set([...completedQuests, day])].sort((a, b) => a - b);
}
