import { deepStrictEqual, equal, throws } from "node:assert";
import test from "node:test";
import { canCompleteQuest, completeQuest, resolveProgress, type BadgeDefinition, type QuestDefinition } from "./index.js";

const quests: QuestDefinition[] = Array.from({ length: 30 }, (_, index) => {
  const day = index + 1;
  return { day, type: [5, 10, 15, 20].includes(day) ? "checkpoint" : day === 30 ? "final_exam" : "lesson" };
});

const badges: BadgeDefinition[] = [
  { id: "rookie-i", unlockDay: 1, requires: [] },
  { id: "rookie-ii", unlockDay: 2, requires: [1] },
  { id: "rookie-iii", unlockDay: 3, requires: [1, 2] },
  { id: "rookie-iv", unlockDay: 4, requires: [1, 2, 3] },
  { id: "bronze", unlockDay: 5, requires: [1, 2, 3, 4] },
  { id: "silver", unlockDay: 10, requires: [1, 2, 3, 4, 5, 6, 7, 8, 9] },
  { id: "adept-warrior", unlockDay: 15, requires: [10, 11, 12, 13, 14] },
  { id: "kanji-apprentice", unlockDay: 20, requires: [15, 16, 17, 18, 19] },
  { id: "japan-ready", unlockDay: 25, requires: [20, 21, 22, 23, 24] },
  { id: "interview-master", unlockDay: 29, requires: [25, 26, 27, 28] },
  { id: "gold-jayantara", unlockDay: 30, requires: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29] },
];

const config = { quests, badges };

test("fresh state is canonical", () => {
  deepStrictEqual(resolveProgress([], config), {
    version: 1,
    completedQuests: [],
    xp: 0,
    badges: [],
    currentDay: 1,
    currentPhase: "foundation",
  });
});

test("completion is sequential and idempotent", () => {
  equal(canCompleteQuest(1, []), true);
  equal(canCompleteQuest(3, [1]), false);
  deepStrictEqual(completeQuest(1, []), [1]);
  deepStrictEqual(completeQuest(2, [1]), [1, 2]);
  deepStrictEqual(completeQuest(2, [1, 2]), [1, 2]);
  throws(() => completeQuest(3, []), /requires day-02/);
});

test("milestone progression matches the application contract", () => {
  const state = resolveProgress([1, 2, 3, 4, 5], config);
  equal(state.xp, 650);
  deepStrictEqual(state.badges, ["bronze", "rookie-i", "rookie-ii", "rookie-iii", "rookie-iv"]);
  equal(state.currentDay, 6);
  equal(state.currentPhase, "novice");
});

test("full course produces deterministic final state", () => {
  const state = resolveProgress(Array.from({ length: 30 }, (_, i) => i + 1), config);
  equal(state.xp, 4000);
  equal(state.currentDay, 30);
  equal(state.currentPhase, "career");
  equal(state.badges.includes("gold-jayantara"), true);
  equal(state.completedQuests.length, 30);
  deepStrictEqual(state, resolveProgress([...state.completedQuests].reverse(), config));
});
