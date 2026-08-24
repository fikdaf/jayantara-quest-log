export type ProgressState = {
  completedDays: number[];
};

export interface ProgressStorage {
  load(): Promise<ProgressState>;
  save(state: ProgressState): Promise<void>;
  clear(): Promise<void>;
}

export class MemoryProgressStorage implements ProgressStorage {
  private state: ProgressState = { completedDays: [] };

  async load(): Promise<ProgressState> {
    return { completedDays: [...this.state.completedDays] };
  }

  async save(state: ProgressState): Promise<void> {
    this.state = { completedDays: [...state.completedDays] };
  }

  async clear(): Promise<void> {
    this.state = { completedDays: [] };
  }
}
