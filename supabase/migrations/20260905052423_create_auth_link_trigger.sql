/*
# Campus360 — Auto-link Auth Users to Profile Tables

## Overview
Creates a trigger that runs AFTER a new auth user signs up.
It searches the students, faculty, and admin tables for a row with a matching
email and sets the user_id column on that row. This way, when a user signs up
with an email that already exists in the profile table (seeded by admin),
they are automatically linked and can access their role-specific dashboard.

## How It Works
1. User signs up via Supabase Auth with email + password.
2. Trigger fires on INSERT to auth.users.
3. It checks students, then faculty, then admin for a matching email.
4. If found, it sets user_id on the matching row.
5. The AuthContext in the frontend then loads the profile by user_id.

## Security
- The trigger function runs as SECURITY DEFINER with search_path set to public.
- It only runs on auth user creation — not user-modifiable.
*/

CREATE OR REPLACE FUNCTION public.link_auth_user_to_profile()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  -- Try to link to a student profile
  UPDATE students SET user_id = NEW.id
  WHERE email = NEW.email AND user_id IS NULL;

  -- If not linked to student, try faculty
  IF NOT FOUND THEN
    UPDATE faculty SET user_id = NEW.id
    WHERE email = NEW.email AND user_id IS NULL;
  END IF;

  -- If still not linked, try admin
  IF NOT FOUND THEN
    UPDATE admin SET user_id = NEW.id
    WHERE username = NEW.email AND user_id IS NULL;
  END IF;

  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.link_auth_user_to_profile();
