/**
 * Centralized TypeScript Type Definitions for Universal Pro AI
 * =============================================================
 * Enforces strict null-safety and historical cache compatibility
 * across all domain extractions (Cooking, Fitness, Travel, Tech).
 */

export interface NutritionInfo {
  calories?: number;
  protein_g?: number;
  carbs_g?: number;
  fat_g?: number;
  is_estimated?: boolean;
}

export interface ProductItem {
  name: string;
  price?: string;
  search_query?: string;
  links?: {
    amazon?: string;
    flipkart?: string;
    blinkit?: string;
    zepto?: string;
  };
}

export interface ResourceItem {
  name: string;
  platform?: string;
  search_query?: string;
}

export interface ExtractionResult {
  category?: string;
  category_name?: string;
  emoji?: string;
  title?: string;
  recipe_title?: string;
  summary?: string;
  dish_type?: string;
  workout_split?: string;
  difficulty?: string;
  prep_time?: string;
  cooking_time?: string;
  servings?: number;
  ingredients?: any[];
  instructions?: string[];
  equipment_needed?: string[];
  chef_tips?: string[];
  products?: ProductItem[];
  resources?: ResourceItem[];
  details?: string;
  source_url?: string;
  full_text?: string;
  media_url?: string;
  thumbnail_url?: string;
  cached?: boolean;
  audio_song?: string;
  reel_language?: string;
  notes_english?: string;
  notes_original_language?: string;
  google_maps_locations?: Array<{ name: string; query: string; maps_url: string }>;
  travel_itinerary?: Array<{ day: string; activities: Array<{ description: string; location_name?: string; maps_url?: string }> }>;
  nutrition?: NutritionInfo;
}

export type RecipeSchema = ExtractionResult;
