import axios from "axios";
import type { LivabilityInput, LivabilityPrediction } from "@/types/livability";

export const API = axios.create({
  baseURL: "http://localhost:8000",
});

export async function predictLivability(
  body: LivabilityInput
): Promise<LivabilityPrediction> {
  const { data } = await API.post<LivabilityPrediction>("/api/v1/predict", body);
  return data;
}
