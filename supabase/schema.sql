-- NutriMind AI — Supabase PostgreSQL schema
-- Run this in Supabase Dashboard → SQL Editor

CREATE TABLE IF NOT EXISTS meals (
    id TEXT PRIMARY KEY,
    food_name TEXT NOT NULL,
    image_url TEXT,
    nutrition_json JSONB NOT NULL,
    health_score INTEGER NOT NULL,
    ingredients_json JSONB NOT NULL,
    actions_json JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_meals_created_at ON meals (created_at DESC);

-- Optional: Supabase Storage bucket for meal images
-- Create bucket named "meal-images" in Storage → New bucket (public)
