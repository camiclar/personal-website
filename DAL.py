import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re

DB_PATH = Path('projects.db')


def get_connection() -> sqlite3.Connection:
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn


def init_db() -> None:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute(
			"""
			CREATE TABLE IF NOT EXISTS projects (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				slug TEXT UNIQUE NOT NULL,
				title TEXT NOT NULL,
				description TEXT NOT NULL,
				image_file_name TEXT NOT NULL
			);
			"""
		)
		conn.commit()


def seed_projects() -> None:
	# Only seed if table is empty
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT COUNT(1) as c FROM projects")
		count = cursor.fetchone()[0]
		if count:
			return

		projects: List[Tuple[str, str, str, str]] = [
			(
				'iu-mobile',
				'IU Mobile User Feedback',
				'Collecting feedback and discovering insights to direct focus for future updates.',
				'iu-mobile-sentiments.jpg',
			),
			(
				'building-a-mind',
				'Building A Mind UI',
				'Designing a user interface for a computer vision AI model and creating beginner-friendly documentation.',
				'bam-preview.jpg',
			),
			(
				'resource-library',
				'Career Resource Library',
				'Migrating nearly 400 career resources and adding additional filter functionality to improve user experience and future-proof the library.',
				'resource-library-preview.jpg',
			),
		]

		cursor.executemany(
			"INSERT INTO projects (slug, title, description, image_file_name) VALUES (?, ?, ?, ?)",
			projects,
		)
		conn.commit()


def get_all_projects() -> List[Dict]:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM projects ORDER BY id ASC")
		rows = cursor.fetchall()
		return [dict(row) for row in rows]


def get_project_by_slug(slug: str) -> Optional[Dict]:
	with get_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM projects WHERE slug = ?", (slug,))
		row = cursor.fetchone()
		return dict(row) if row else None


def _slugify(title: str) -> str:
	# basic slugify: lowercase, replace non-alphanum with hyphens
	s = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-").lower()
	return s or "project"


def _unique_slug(conn: sqlite3.Connection, base_slug: str) -> str:
	slug = base_slug
	index = 1
	cur = conn.cursor()
	while True:
		cur.execute("SELECT 1 FROM projects WHERE slug = ?", (slug,))
		if cur.fetchone() is None:
			return slug
		index += 1
		slug = f"{base_slug}-{index}"


def insert_project(title: str, description: str, image_file_name: str) -> Dict:
	"""Insert a new project and return the created row as dict."""
	with get_connection() as conn:
		cursor = conn.cursor()
		base = _slugify(title)
		slug = _unique_slug(conn, base)
		cursor.execute(
			"INSERT INTO projects (slug, title, description, image_file_name) VALUES (?, ?, ?, ?)",
			(slug, title, description, image_file_name),
		)
		conn.commit()
		cursor.execute("SELECT * FROM projects WHERE slug = ?", (slug,))
		row = cursor.fetchone()
		return dict(row)
