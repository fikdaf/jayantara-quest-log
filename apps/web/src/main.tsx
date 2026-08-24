import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { canCompleteQuest, completeQuest, resolveProgress, type ProgressConfig } from "@jayantara/core";
import "./style.css";

const STORAGE_KEY = "jayantara.completed-quests";
const quests = Array.from({ length: 30 }, (_, i) => ({ day: i + 1, type: i === 29 ? "final_exam" as const : (i + 4) % 5 === 0 ? "checkpoint" as const : "lesson" as const }));
const badges = [
  { id: "bronze", unlockDay: 5, requires: [1, 2, 3, 4, 5] }, { id: "silver", unlockDay: 10, requires: [6, 7, 8, 9, 10] },
  { id: "adept-warrior", unlockDay: 15, requires: [11, 12, 13, 14, 15] }, { id: "kanji-apprentice", unlockDay: 20, requires: [16, 17, 18, 19, 20] },
  { id: "japan-ready", unlockDay: 25, requires: [21, 22, 23, 24, 25] }, { id: "interview-master", unlockDay: 29, requires: [26, 27, 28, 29] },
  { id: "gold-jayantara", unlockDay: 30, requires: Array.from({ length: 30 }, (_, i) => i + 1) },
];
const config: ProgressConfig = { quests, badges };
function readCompleted(): number[] { try { return JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "[]"); } catch { return []; } }

function App() {
  const [completed, setCompleted] = useState<number[]>(readCompleted);
  useEffect(() => localStorage.setItem(STORAGE_KEY, JSON.stringify(completed)), [completed]);
  const state = useMemo(() => resolveProgress(completed, config), [completed]);
  const progress = Math.round((state.completedQuests.length / 30) * 100);
  function finish(day: number) { if (canCompleteQuest(day, completed)) setCompleted((current) => completeQuest(day, current)); }
  return <main className="app-shell">
    <header className="topbar"><div><p className="eyebrow">JAYANTARA</p><h1>Nihongo Master-Kit</h1></div><button className="ghost" onClick={() => setCompleted([])}>Reset</button></header>
    <section className="dashboard"><div className="progress-card"><div className="progress-heading"><div><span>Current quest</span><strong>Day {String(state.currentDay).padStart(2, "0")}</strong></div><div className="xp">{state.xp} XP</div></div><div className="bar"><i style={{ width: `${progress}%` }} /></div><div className="progress-meta"><span>{state.currentPhase}</span><span>{state.completedQuests.length}/30 complete</span></div></div>
      <div className="stats"><article><strong>{state.completedQuests.length}</strong><span>Completed</span></article><article><strong>{state.badges.length}</strong><span>Badges</span></article><article><strong>{progress}%</strong><span>Progress</span></article></div></section>
    <section className="quests"><div className="section-title"><h2>Quest path</h2><span>Day N requires Day N−1</span></div><div className="quest-grid">{quests.map((quest) => { const done = completed.includes(quest.day); const available = done || canCompleteQuest(quest.day, completed); return <button key={quest.day} className={`quest ${done ? "done" : ""} ${!available ? "locked" : ""}`} disabled={done || !available} onClick={() => finish(quest.day)}><span className="quest-day">{String(quest.day).padStart(2, "0")}</span><span className="quest-type">{quest.type.replace("_", " ")}</span><span className="status">{done ? "✓" : available ? "Start" : "🔒"}</span></button>; })}</div></section>
    <section className="badges"><div className="section-title"><h2>Badges</h2><span>{state.badges.length} unlocked</span></div><div className="badge-row">{badges.map((badge) => <div className={`badge ${state.badges.includes(badge.id) ? "unlocked" : ""}`} key={badge.id}><span>◆</span><strong>{badge.id}</strong></div>)}</div></section>
  </main>;
}
createRoot(document.getElementById("root")!).render(<React.StrictMode><App /></React.StrictMode>);
