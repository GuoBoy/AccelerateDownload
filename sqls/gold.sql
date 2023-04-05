/*
 Navicat Premium Data Transfer

 Source Server         : corn_monitor
 Source Server Type    : SQLite
 Source Server Version : 3035005 (3.35.5)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005 (3.35.5)
 File Encoding         : 65001

 Date: 05/03/2023 18:15:05
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for gold
-- ----------------------------
DROP TABLE IF EXISTS "gold";
CREATE TABLE "gold" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "price" NUMBER,
  "date" DATE
);

-- ----------------------------
-- Auto increment value for gold
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 1 WHERE name = 'gold';

PRAGMA foreign_keys = true;
