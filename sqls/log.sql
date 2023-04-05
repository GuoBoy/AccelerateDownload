/*
 Navicat Premium Data Transfer

 Source Server         : corn_monitor
 Source Server Type    : SQLite
 Source Server Version : 3035005 (3.35.5)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005 (3.35.5)
 File Encoding         : 65001

 Date: 05/03/2023 10:09:32
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for log
-- ----------------------------
DROP TABLE IF EXISTS "log";
CREATE TABLE "log" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "message" TEXT NOT NULL,
  "created_at" timestamp
);

PRAGMA foreign_keys = true;
