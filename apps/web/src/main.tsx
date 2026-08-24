import React from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

function App() {
  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">JAYANTARA</p>
        <h1>Nihongo Master-Kit</h1>
        <p className="lead">30 quests. One progressive path to practical Japanese.</p>
        <div className="actions">
          <button type="button">Start Day 01</button>
          <button type="button" className="secondary">View Progress</button>
        </div>
      </section>
      <section className="card-grid" aria-label="Program overview">
        <article><strong>30</strong><span>Quests</span></article>
        <article><strong>6</strong><span>Phases</span></article>
        <article><strong>∞</strong><span>Practice</span></article>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode><App /></React.StrictMode>,
);
