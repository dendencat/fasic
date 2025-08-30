# AGENT.md — Codex CLI エージェント定義

> プロジェクト: **SwipeTune**（自動音楽生成 × マッチング式スワイプのクロスプラットフォームRNアプリ）  
> 目的: **Codex CLI**（開発エージェント）で、MVPを**計画→実装→テスト→実行**まで自動化するための仕様書

---

## 1. ミッション（GOAL / NON-GOAL）

### GOAL

- React Native（Expo）+ NativeWind を用いた**ネイティブMVP**の実装
    
- 音楽の**再生/停止/次/前**、**履歴**、**スワイプ（like/dislike/skip）**、**エクスプローラ**、**アップロード**、**生成（API経由）**、**マイリスト/プレイリスト**の実装
    
- FastAPI バックエンド + Postgres（Supabase可）+ S3 互換ストレージで API/永続化
    
- 生成は**外部音楽生成API**をサーバー経由で呼ぶ（キーはクライアントに出さない）
    

### NON-GOAL

- 本番級のレコメンド（MVPでは**ルールベース + 近傍検索の雰囲気**まで）
    
- 複雑なモデレーション/著作権審査（MVPでは**長さ制限/拡張子/レビューフラグ**のみ）
    
- マルチリージョン/高可用性構成（単一リージョンでOK）
    

---

## 2. 技術スタックと選定

**フロント（Expo/React Native）**

- UI: **NativeWind**（Tailwind 互換）
    
- Icons: **lucide-react-native**（要 `react-native-svg`）
    
- 再生: **react-native-track-player**
    
- スワイプ: **react-native-gesture-handler** + **react-native-reanimated**
    
- アニメーション補助: **Moti**（任意）
    

**サーバ**

- API: **FastAPI**（Python 3.11+）
    
- DB: **Postgres**（`pgvector` は将来拡張）、ORMは **SQLModel** or **SQLAlchemy**
    
- ストレージ: **S3/R2** 互換（署名URLアップロード）
    
- ジョブ: **RQ** or **Celery**（シンプルなら同期→後で非同期化）
    
- Realtime/通知（任意）: WebSocket / SSE
    

---

## 3. リポジトリ構成（monorepo）

bash

コピーする編集する

`/swipetune   /apps     /mobile      # Expo (React Native)     /server      # FastAPI   /packages     /ui          # 共通UI（将来）     /types       # OpenAPIベースの型共有（将来）   /infra     docker-compose.yml     .env.example   AGENT.md       # ← このファイル   README.md`

---

## 4. 環境変数

`.env`（ルート or 各サービス配下）:

ini

コピーする編集する

`# Server API_PORT=8080 DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/swipetune S3_ENDPOINT=http://localhost:9000 S3_BUCKET=swipetune-tracks S3_ACCESS_KEY=localkey S3_SECRET_KEY=localsecret S3_REGION=ap-northeast-1 MUSIC_GEN_API_BASE=https://<provider-api> MUSIC_GEN_API_KEY=sk-xxxx ALLOWED_ORIGINS=http://localhost:8081  # Mobile EXPO_PUBLIC_API_BASE=http://localhost:8080`

---

## 5. Codex CLI エージェントの行動方針

1. **プラン生成**: 本書の「タスクグラフ」に従い、作業計画（ステップ/所要成果物/検証方法）を出力
    
2. **環境準備**: `docker-compose` で DB/S3 を起動、サーバ→クライアントの順に `dev` 起動
    
3. **テスト駆動**: バックエンドは **pytest**、モバイルは**基本動作E2E**（Expo Goで手動検証）
    
4. **小さくコミット**: 機能単位で PR 作成、lint/format を通す
    
5. **自己検証**: API Contract（OpenAPI）と実装を常に合致させる
    
6. **セキュア実装**: 生成APIは**サーバ経由**。クライアントにキーを渡さない
    
7. **記録**: `CHANGELOG.md` と **/server/OPENAPI.yaml** を更新し続ける
    

**使用できるコマンド（例）**

bash

コピーする編集する

`# ルート make up               # docker-compose up -d（DB/S3） make down             # 停止 make gen-openapi      # サーバのOpenAPIを書き出し  # server cd apps/server python -m venv .venv && source .venv/bin/activate pip install -e ".[dev]" uvicorn app.main:app --reload --port 8080 pytest -q  # mobile cd apps/mobile pnpm install pnpm expo start`

---

## 6. タスクグラフ（MVP・2週間想定）

### T1: 雛形生成

- `apps/server`: FastAPI 初期化、/health 実装、DB 接続、S3 クライアント
    
- `apps/mobile`: Expo + NativeWind + lucide + gesture-handler + reanimated 設定
    

**完了条件**: `/health=200`、RNで「Hello + 再生UIの枠」表示

### T2: 再生キュー

- `react-native-track-player` のセットアップ（バックグラウンド権限）
    
- `Play/Pause/Next/Prev` と現在曲の表示
    

**完了条件**: 任意のURLをキュー投入→再生/停止/スキップが動く

### T3: DB/モデル/マイグレーション

- `users, tracks, interactions, play_events, playlists, playlist_items, jobs`
    
- Alembic でマイグレーション
    

**完了条件**: CRUD と簡易 seed スクリプト

### T4: アップロード（署名URL）

- `POST /tracks/upload-url`（認証は一旦なし）→ 署名URL発行
    
- クライアントから直PUT→完了後 `POST /tracks/commit` でDB登録
    

**完了条件**: 端末ファイル→S3 へアップ→アプリで再生できる

### T5: エクスプローラ & スワイプ

- `GET /explore?cursor=`（新着ソート、like 多めブースト）
    
- スワイプUI（like/dislike/skip）→ `POST /interactions`
    

**完了条件**: 10曲供給→スワイプの記録がDBに残る

### T6: 履歴 & プレイリスト

- `GET /history`, `POST /playlists`, `POST /playlists/{id}/items`
    

**完了条件**: 再生完了/スキップを履歴表示。プレイリストへ追加できる

### T7: 生成ジョブ（API 経由）

- `POST /generate` → 外部API呼び出し（同期/初期版）。結果をS3へ保存し `tracks` 登録
    
- 後続で非同期化（RQ/Celery）とWebhook
    

**完了条件**: テキストプロンプト→生成曲→即再生できる

---

## 7. API コントラクト（抜粋 / draft）

**共通**

- BaseURL: `${EXPO_PUBLIC_API_BASE}`（例: `http://localhost:8080`）
    
- `Content-Type: application/json`
    

yaml

コピーする編集する

`GET /health 200: { "ok": true, "version": "x.y.z" }  GET /explore?cursor={string} 200: {   "items": [Track],   "nextCursor": "..." }  POST /interactions body: { "trackId": string, "type": "like" | "dislike" | "skip" } 201: { "ok": true }  GET /history?limit=50 200: [ { "trackId": "...", "action": "play|skip|complete", "ts": "ISO" } ]  POST /tracks/upload-url body: { "filename": "foo.mp3", "contentType": "audio/mpeg" } 200: { "uploadUrl": "https://...", "objectKey": "tracks/uuid.mp3" }  POST /tracks/commit body: { "objectKey": "tracks/uuid.mp3", "meta": { "title": "name", "duration": 42 } } 201: Track  POST /playlists body: { "title": "My List", "isPublic": false } 201: Playlist  POST /playlists/{id}/items body: { "trackId": string } 201: { "ok": true }  POST /generate body: { "prompt": "lofi hiphop 90bpm", "durationSec": 30 } 201: { "jobId": "uuid", "status": "completed", "track": Track } # MVPは同期`

**型**

ts

コピーする編集する

`type Track = {   id: string;   ownerId: string | null;   url: string;            // S3 署名URL or 公開URL   cover?: string | null;   duration?: number;   bpm?: number | null;   key?: string | null;   genres?: string[];   createdAt: string;      // ISO };  type Playlist = {   id: string;   ownerId: string;   title: string;   isPublic: boolean;   createdAt: string; };`

---

## 8. クライアント主要フロー

### 再生

1. `TrackPlayer.setupPlayer()` 初期化
    
2. `TrackPlayer.add([ { id, url, title } ])`
    
3. `Play/Pause/Next/Prev` ボタンで制御
    
4. イベント `playback-track-changed` → `/play_events` へ `play/complete/skip` をPOST（後回し可）
    

### スワイプ

- `PanGestureHandler` でX/Yを追跡し閾値で判定
    
- `like/dislike/skip` をPOST → 次カードをフェッチ
    
- フィードは `GET /explore`（ページング／cursor）
    

### アップロード

- `POST /tracks/upload-url` → 署名URL取得
    
- RNから `PUT`（`fetch` or `axios`）
    
- `POST /tracks/commit` でDB登録→即再生
    

### 生成

- `POST /generate`（プロンプト）→ 完了レスに `track.url`
    
- キューに追加→再生
    

---

## 9. データモデル（SQL 概要）

sql

コピーする編集する

`CREATE TABLE users (   id uuid PRIMARY KEY,   name text );  CREATE TABLE tracks (   id uuid PRIMARY KEY,   owner_id uuid NULL,   url text NOT NULL,   cover text NULL,   duration int NULL,   bpm int NULL,   key text NULL,   genres text[] NULL,   created_at timestamptz NOT NULL DEFAULT now() );  CREATE TABLE interactions (   user_id uuid,   track_id uuid,   type text CHECK (type IN ('like','dislike','skip')),   ts timestamptz NOT NULL DEFAULT now() );  CREATE TABLE play_events (   user_id uuid,   track_id uuid,   action text CHECK (action IN ('play','complete','skip')),   ts timestamptz NOT NULL DEFAULT now() );  CREATE TABLE playlists (   id uuid PRIMARY KEY,   owner_id uuid NOT NULL,   title text NOT NULL,   is_public boolean NOT NULL DEFAULT false,   created_at timestamptz NOT NULL DEFAULT now() );  CREATE TABLE playlist_items (   playlist_id uuid REFERENCES playlists(id),   track_id uuid REFERENCES tracks(id),   "order" int NOT NULL DEFAULT 0,   PRIMARY KEY (playlist_id, track_id) );  CREATE TABLE jobs (   id uuid PRIMARY KEY,   user_id uuid,   type text NOT NULL,        -- 'generate'   status text NOT NULL,      -- 'queued'|'running'|'completed'|'failed'   result_track_id uuid NULL,   created_at timestamptz NOT NULL DEFAULT now(),   updated_at timestamptz NOT NULL DEFAULT now() );`

---

## 10. セキュリティ/コンプラ最小ルール

- 生成APIキーは**サーバのみ**で保持。クライアントから直接呼ばない
    
- アップロードは**署名URL**方式、`content-type`/拡張子/最大長（例: 60s/10MB）を制限
    
- CORS は `ALLOWED_ORIGINS` を明示
    
- ログには**個人情報/キー**を出力しない
    
- 著作権: MVPでは**ユーザ同意 + 通報機能**だけ設置（将来は指紋照合/外部審査を検討）
    

---

## 11. 品質ゲート

- `apps/server`: `pytest` 全通過、`ruff`/`black` パス
    
- `apps/mobile`: TypeScript `tsc --noEmit`、ESLint パス
    
- E2E: 主要フロー（再生/スワイプ/アップロード/生成）が**手順書通り**に動作
    
- OpenAPI（/server/OPENAPI.yaml）と実装の差分なし
    

---

## 12. エージェント実行レシピ（Codex CLI）

### bootstrap

markdown

コピーする編集する

`- plan:    - create monorepo folders    - init FastAPI with poetry/pdm or uv    - init Expo (TypeScript)    - add NativeWind, lucide-react-native, gesture-handler, reanimated, track-player    - write docker-compose (postgres, minio)    - write .env.example - run:    - docker-compose up -d    - server dev up (uvicorn)    - mobile dev up (expo start) - verify:    - GET /health -> 200    - Mobile shows placeholder UI - commit: "chore: bootstrap server/mobile/infra"`

### implement: playback

sql

コピーする編集する

`- add track-player setup (bg service for iOS/Android) - build NowPlaying screen with controls - smoke test with remote mp3 url - commit: "feat(mobile): playback with track-player"`

### implement: upload + commit

pgsql

コピーする編集する

`- server: POST /tracks/upload-url, /tracks/commit - mobile: pick doc -> PUT to signed url -> commit -> add to queue - commit: "feat: signed upload and commit"`

### implement: explore + swipe

pgsql

コピーする編集する

`- server: GET /explore, POST /interactions - mobile: SwipeDeck (gesture-handler + reanimated) - commit: "feat: explore feed and swipe interactions"`

### implement: history + playlist

diff

コピーする編集する

`- server/mobile endpoints and screens - commit`

### implement: generate (sync MVP)

pgsql

コピーする編集する

`- server: POST /generate -> call external API -> save to S3 -> return track - mobile: prompt input -> call -> enqueue track - commit`

---

## 13. 画面一覧 & ルーティング（モバイル）

- `/now` 再生中（Play/Pause/Next/Prev、シーク、アートワーク）
    
- `/explore` スワイプデッキ（like/dislike/skip）
    
- `/generate` 生成フォーム（プロンプト・秒数）
    
- `/library` 自分の曲/アップロード/プレイリスト
    
- `/history` 最近の再生・スキップ
    

Tab 4本（Now | Explore | Generate | Library）＋ History は Library 内部から遷移

---

## 14. スワイプ判定仕様（閾値）

- `tx`（X移動）> +80px → **like**
    
- `tx` < -80px → **dislike**
    
- `|ty|` > 120px or 中央戻り → **skip**
    
- 判定時に `POST /interactions`、次カードを `GET /explore` で補充
    

---

## 15. 簡易レコメンド（MVP）

- `score = 0.6*recent_like_author + 0.2*global_popular + 0.2*recency_boost`
    
- 同一ユーザ連投は間引き、未視聴優先
    

---

## 16. 将来拡張

- ジョブ非同期化（RQ/Celery + Redis、Webhook→SSE）
    
- `pgvector` で CLAP 埋め込み格納 → 類似曲推薦
    
- Auth（Supabase Auth or Cognito）
    
- オフライン再生/ダウンロード
    
- モデレーション/指紋照合
    

---

## 17. 受け入れ基準（Definition of Done）

- スマホ（iOS/Android）で
    
    - 外部URL/アップロード済み曲の**再生**ができる
        
    - **Explore でスワイプ**でき記録が残る
        
    - **Generate**でプロンプトから曲が1本生成され再生できる
        
    - **Playlist**へ追加/再生できる
        
    - クラッシュなし、主要画面で60fpsに近い操作感
        

---

## 18. 既知のリスク

- 生成APIの**利用規約/商用可否**は要確認（テストキーと本番キー分離）
    
- iOS のバックグラウンド権限（Audio）設定漏れによる停止
    
- 大容量アップロードの帯域/コスト
    
- 著作権侵害アップロードの取り扱い（通報・削除フローの整備が必要）
