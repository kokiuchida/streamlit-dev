"""Git command 1000-knock questions database."""

QUESTIONS = [
    # ===== Level 1: Basics =====
    {
        "id": 1,
        "level": 1,
        "category": "初期化・設定",
        "question": "カレントディレクトリをGitリポジトリとして初期化するコマンドは？",
        "answer": ["git init"],
        "hint": "まずリポジトリを「init」する必要があります。",
        "explanation": (
            "**`git init`** は、カレントディレクトリに `.git/` という隠しディレクトリを作成し、"
            "Gitリポジトリとして初期化します。\n\n"
            "- `.git/` にはコミット履歴・設定・ブランチ情報などすべてのメタデータが格納されます。\n"
            "- `git init <ディレクトリ名>` で新規ディレクトリを作成しつつ初期化することも可能です。\n"
            "- すでに `.git/` が存在する場合に実行しても安全です（再初期化になるだけ）。"
        ),
    },
    {
        "id": 2,
        "level": 1,
        "category": "リモート・クローン",
        "question": "リモートリポジトリ `https://github.com/user/repo.git` をローカルにクローンするコマンドは？",
        "answer": ["git clone https://github.com/user/repo.git"],
        "hint": "リポジトリを「複製」する操作です。",
        "explanation": (
            "**`git clone <URL>`** は、指定したリモートリポジトリをローカルにコピーします。\n\n"
            "- `origin` という名前でリモートが自動登録されます。\n"
            "- `git clone <URL> <ディレクトリ名>` でクローン先フォルダ名を指定可能。\n"
            "- `--depth 1` を付けると最新コミットのみ取得する浅いクローンになります（高速化に有効）。"
        ),
    },
    {
        "id": 3,
        "level": 1,
        "category": "ステージング",
        "question": "ファイル `README.md` をステージング（インデックスに追加）するコマンドは？",
        "answer": ["git add README.md"],
        "hint": "変更をコミット前に「追加」します。",
        "explanation": (
            "**`git add <ファイル>`** は、ワーキングツリーの変更をインデックス（ステージングエリア）に追加します。\n\n"
            "- `git add .` でカレントディレクトリ以下のすべての変更をステージできます。\n"
            "- `git add -p` で変更を hunk 単位で選択的にステージできます（推奨）。\n"
            "- ステージした内容だけがコミットに含まれます。"
        ),
    },
    {
        "id": 4,
        "level": 1,
        "category": "コミット",
        "question": "ステージした変更を `\"first commit\"` というメッセージでコミットするコマンドは？",
        "answer": ['git commit -m "first commit"', "git commit -m 'first commit'"],
        "hint": "`-m` オプションでメッセージを指定します。",
        "explanation": (
            "**`git commit -m \"<メッセージ>\"`** は、ステージングエリアの内容を1つのスナップショットとして記録します。\n\n"
            "- `-m` を省略するとエディタが開きます。\n"
            "- `git commit --amend` で直前のコミットメッセージや内容を修正できます。\n"
            "- コミットにはSHA-1ハッシュが付与され、永続的な識別子になります。"
        ),
    },
    {
        "id": 5,
        "level": 1,
        "category": "状態確認",
        "question": "ワーキングツリーとステージングエリアの状態を確認するコマンドは？",
        "answer": ["git status"],
        "hint": "現在の「状態」を見るコマンドです。",
        "explanation": (
            "**`git status`** は、追跡ファイルの変更・未追跡ファイル・ステージ済みの変更を表示します。\n\n"
            "- `git status -s` で短縮形式（short）の表示になります。\n"
            "- `??` は未追跡、`M` は変更あり、`A` はステージ済みを示します。\n"
            "- コミット前に必ず確認する習慣をつけましょう。"
        ),
    },
    {
        "id": 6,
        "level": 1,
        "category": "ログ",
        "question": "コミット履歴を一覧表示するコマンドは？",
        "answer": ["git log"],
        "hint": "過去の「記録」を見るコマンドです。",
        "explanation": (
            "**`git log`** は、コミット履歴をハッシュ・著者・日時・メッセージと共に表示します。\n\n"
            "- `git log --oneline` で1行表示（ハッシュ先頭7文字+メッセージ）になります。\n"
            "- `git log --graph --oneline --all` でブランチの分岐をグラフ表示できます。\n"
            "- `git log -n 5` で最新5件だけ表示します。"
        ),
    },
    {
        "id": 7,
        "level": 1,
        "category": "差分確認",
        "question": "ワーキングツリーとインデックスの差分（未ステージの変更）を確認するコマンドは？",
        "answer": ["git diff"],
        "hint": "変更の「差分」を見るコマンドです。",
        "explanation": (
            "**`git diff`** は、ワーキングツリーとステージングエリア（インデックス）の差分を表示します。\n\n"
            "- `git diff --staged`（または `--cached`）でステージ済みの変更とHEADの差分を確認できます。\n"
            "- `git diff HEAD` でワーキングツリーとHEADの全差分を見られます。\n"
            "- `git diff <ブランチ1>..<ブランチ2>` でブランチ間の差分も確認可能です。"
        ),
    },
    {
        "id": 8,
        "level": 1,
        "category": "リモート",
        "question": "リモートリポジトリ `origin` の `main` ブランチに変更をプッシュするコマンドは？",
        "answer": ["git push origin main"],
        "hint": "ローカルの変更をリモートに「押し出す」操作です。",
        "explanation": (
            "**`git push <リモート名> <ブランチ名>`** は、ローカルのコミットをリモートリポジトリに送信します。\n\n"
            "- 初回は `git push -u origin main` で上流ブランチを設定すると、以降は `git push` だけでOKです。\n"
            "- `--force`（`-f`）は強制プッシュで履歴を上書きします。チームでの使用は要注意。\n"
            "- `--force-with-lease` は、リモートが自分の知らない更新を持っていれば失敗するより安全な強制プッシュです。"
        ),
    },
    {
        "id": 9,
        "level": 1,
        "category": "リモート",
        "question": "リモートリポジトリ `origin` の `main` ブランチから変更を取得してマージするコマンドは？",
        "answer": ["git pull origin main", "git pull"],
        "hint": "リモートの変更を「引っ張る」操作です。",
        "explanation": (
            "**`git pull`** は、`git fetch` と `git merge` を組み合わせた操作です。\n\n"
            "- `git pull --rebase` を使うとマージコミットを作らずにリベース形式で取り込めます（履歴が綺麗になります）。\n"
            "- `git fetch` だけ先に実行して差分を確認してからマージする習慣も良いです。\n"
            "- `git pull origin main` は `origin/main` から現在のブランチへ取り込みます。"
        ),
    },
    {
        "id": 10,
        "level": 1,
        "category": "設定",
        "question": "Gitのグローバル設定でユーザー名を `Taro Yamada` に設定するコマンドは？",
        "answer": ['git config --global user.name "Taro Yamada"', "git config --global user.name 'Taro Yamada'"],
        "hint": "`--global` オプションと `user.name` キーを使います。",
        "explanation": (
            "**`git config --global user.name \"<名前>\"`** は、すべてのリポジトリに適用されるグローバル設定を行います。\n\n"
            "- 設定は `~/.gitconfig` に保存されます。\n"
            "- `--local`（デフォルト）はリポジトリ固有、`--system` はシステム全体の設定です。\n"
            "- `git config --global user.email` でメールアドレスも設定しましょう。"
        ),
    },
    # ===== Level 2: Branching =====
    {
        "id": 11,
        "level": 2,
        "category": "ブランチ",
        "question": "新しいブランチ `feature/login` を作成するコマンドは？",
        "answer": ["git branch feature/login"],
        "hint": "`git branch` コマンドにブランチ名を指定します。",
        "explanation": (
            "**`git branch <ブランチ名>`** は、現在のHEADを起点として新しいブランチを作成します。\n\n"
            "- このコマンドはブランチを作るだけで、切り替えは行いません。\n"
            "- `git checkout -b feature/login` または `git switch -c feature/login` で作成+切り替えを同時に行えます。\n"
            "- `git branch` だけでブランチ一覧を表示します（`-a` でリモートも含む）。"
        ),
    },
    {
        "id": 12,
        "level": 2,
        "category": "ブランチ",
        "question": "ブランチ `feature/login` に切り替えるコマンドは？（`git switch` を使ってください）",
        "answer": ["git switch feature/login"],
        "hint": "Git 2.23以降で推奨されるブランチ切り替えコマンドです。",
        "explanation": (
            "**`git switch <ブランチ名>`** は Git 2.23 で導入されたブランチ切り替え専用コマンドです。\n\n"
            "- 従来の `git checkout <ブランチ名>` と同等ですが、意図がより明確です。\n"
            "- `git switch -c <新ブランチ名>` で作成と切り替えを同時に行えます。\n"
            "- `git switch -` で直前のブランチに戻れます。"
        ),
    },
    {
        "id": 13,
        "level": 2,
        "category": "ブランチ",
        "question": "ブランチ `feature/login` を `main` にマージするコマンドは？（現在 `main` ブランチにいる前提）",
        "answer": ["git merge feature/login"],
        "hint": "ブランチを「合流」させるコマンドです。",
        "explanation": (
            "**`git merge <ブランチ名>`** は、指定ブランチの変更を現在のブランチに取り込みます。\n\n"
            "- Fast-forward マージ：直線的に進める場合。マージコミットは作られません。\n"
            "- `--no-ff` オプションを付けると、常にマージコミットを作成します（履歴が明確になります）。\n"
            "- コンフリクトが発生した場合はファイルを手動で修正し `git add` → `git commit` します。"
        ),
    },
    {
        "id": 14,
        "level": 2,
        "category": "ブランチ",
        "question": "ローカルブランチ `feature/login` を削除するコマンドは？",
        "answer": ["git branch -d feature/login"],
        "hint": "`-d` オプションで削除します（マージ済みのみ）。",
        "explanation": (
            "**`git branch -d <ブランチ名>`** は、マージ済みブランチを安全に削除します。\n\n"
            "- `-D`（大文字）は未マージでも強制削除します。使用時は注意が必要です。\n"
            "- リモートブランチを削除するには `git push origin --delete <ブランチ名>` を使います。\n"
            "- `git branch --merged` でマージ済みブランチの一覧を確認できます。"
        ),
    },
    {
        "id": 15,
        "level": 2,
        "category": "ブランチ",
        "question": "すべてのローカルおよびリモートブランチを一覧表示するコマンドは？",
        "answer": ["git branch -a"],
        "hint": "「すべて（all）」を意味するオプションを使います。",
        "explanation": (
            "**`git branch -a`** は、ローカルブランチとリモート追跡ブランチの両方を表示します。\n\n"
            "- `git branch` だけでローカルのみ。\n"
            "- `git branch -r` でリモート追跡ブランチのみ。\n"
            "- `git branch -v` でブランチごとの最新コミットも表示されます。"
        ),
    },
    {
        "id": 16,
        "level": 2,
        "category": "タグ",
        "question": "現在のコミットに `v1.0.0` という軽量タグを付けるコマンドは？",
        "answer": ["git tag v1.0.0"],
        "hint": "`git tag` コマンドにタグ名を指定します。",
        "explanation": (
            "**`git tag <タグ名>`** は、現在のHEADに軽量タグ（lightweight tag）を付けます。\n\n"
            "- `git tag -a v1.0.0 -m \"Release 1.0.0\"` で注釈付きタグ（annotated tag）を作成できます。注釈付きタグには作成者・日時・メッセージが含まれます。\n"
            "- `git tag` でタグ一覧表示。\n"
            "- タグはデフォルトで `git push` に含まれません。`git push origin v1.0.0` または `git push --tags` で送信します。"
        ),
    },
    {
        "id": 17,
        "level": 2,
        "category": "スタッシュ",
        "question": "現在の変更を一時的に退避させるコマンドは？",
        "answer": ["git stash", "git stash push"],
        "hint": "変更を「棚上げ」するコマンドです。",
        "explanation": (
            "**`git stash`** は、コミットしていない変更（インデックスとワーキングツリー）を一時的にスタックに保存し、"
            "クリーンな状態に戻します。\n\n"
            "- `git stash list` でスタッシュ一覧を表示。\n"
            "- `git stash pop` で最新のスタッシュを取り出してワーキングツリーに適用します。\n"
            "- `git stash push -m \"作業中の説明\"` でメッセージ付きスタッシュを作れます。\n"
            "- `git stash -u` で未追跡ファイルも含めてスタッシュできます。"
        ),
    },
    {
        "id": 18,
        "level": 2,
        "category": "スタッシュ",
        "question": "スタッシュに退避した変更を取り出して適用するコマンドは？",
        "answer": ["git stash pop"],
        "hint": "スタッシュから「取り出す」コマンドです。",
        "explanation": (
            "**`git stash pop`** は、スタッシュの先頭（最新のもの）を適用し、スタッシュリストから削除します。\n\n"
            "- `git stash apply` は適用してもスタッシュリストに残ります（後で削除が必要）。\n"
            "- `git stash pop stash@{2}` で特定のスタッシュを指定して取り出せます。\n"
            "- コンフリクトが起きた場合は `git stash drop` で手動削除が必要です。"
        ),
    },
    {
        "id": 19,
        "level": 2,
        "category": "リモート",
        "question": "リモートリポジトリの情報を取得するだけでマージしないコマンドは？",
        "answer": ["git fetch", "git fetch origin"],
        "hint": "「取得する」だけでマージはしません。`pull` との違いに注意。",
        "explanation": (
            "**`git fetch`** は、リモートの最新情報をローカルのリモート追跡ブランチに取得しますが、"
            "ワーキングツリーやブランチには影響を与えません。\n\n"
            "- `git fetch` 後に `git diff HEAD origin/main` で差分を確認してからマージできます。\n"
            "- `git pull` = `git fetch` + `git merge` の組み合わせです。\n"
            "- `git fetch --prune` でリモートに存在しないブランチの追跡情報を削除できます。"
        ),
    },
    {
        "id": 20,
        "level": 2,
        "category": "設定",
        "question": "リモートリポジトリ `origin` のURLを確認するコマンドは？",
        "answer": ["git remote -v", "git remote get-url origin"],
        "hint": "リモートの詳細（verbose）を表示するオプションです。",
        "explanation": (
            "**`git remote -v`** は、登録されているリモートリポジトリのURL一覧を表示します（fetch と push 両方）。\n\n"
            "- `git remote show origin` でより詳細な情報（追跡ブランチなど）を確認できます。\n"
            "- `git remote set-url origin <新しいURL>` でURLを変更できます。\n"
            "- `git remote add <名前> <URL>` で新しいリモートを追加できます。"
        ),
    },
    # ===== Level 3: History & Restore =====
    {
        "id": 21,
        "level": 3,
        "category": "履歴操作",
        "question": "直前のコミットを取り消して変更をステージング状態に戻すコマンドは？",
        "answer": ["git reset --soft HEAD~1", "git reset --soft HEAD^"],
        "hint": "`--soft` オプションを使うと変更がステージに残ります。",
        "explanation": (
            "**`git reset --soft HEAD~1`** は、最新コミットを取り消しますが、変更はインデックス（ステージ）に残します。\n\n"
            "- `HEAD~1` は「1つ前のコミット」を意味します。\n"
            "- `--mixed`（デフォルト）：コミットを取り消し、変更はワーキングツリーに戻る（ステージは解除）。\n"
            "- `--hard`：コミットを取り消し、変更も完全に破棄します（危険：復元が難しい）。\n"
            "- すでにプッシュ済みのコミットへの `reset` は避け、`revert` を使いましょう。"
        ),
    },
    {
        "id": 22,
        "level": 3,
        "category": "履歴操作",
        "question": "コミット `abc1234` の変更を打ち消す新しいコミットを作るコマンドは？",
        "answer": ["git revert abc1234"],
        "hint": "変更を「元に戻す」コミットを新たに作成します。",
        "explanation": (
            "**`git revert <コミットハッシュ>`** は、指定コミットの変更を打ち消す新しいコミットを作成します。\n\n"
            "- `git reset` と違い、既存の履歴を書き換えないため、**プッシュ済みのコミットの取り消しに最適**です。\n"
            "- `--no-commit`（`-n`）オプションで複数コミットを一括で取り消してから1つのコミットにまとめられます。\n"
            "- チームでの作業では `reset` より `revert` を優先しましょう。"
        ),
    },
    {
        "id": 23,
        "level": 3,
        "category": "ファイル操作",
        "question": "ステージングされた `main.py` の変更をアンステージ（インデックスから外す）するコマンドは？（`git restore` を使ってください）",
        "answer": ["git restore --staged main.py"],
        "hint": "`--staged` オプションでインデックスから取り出します。",
        "explanation": (
            "**`git restore --staged <ファイル>`** は、ステージングエリアから変更をアンステージします（ワーキングツリーは変わりません）。\n\n"
            "- Git 2.23 以降で推奨される方法です。旧来は `git reset HEAD <ファイル>` を使っていました。\n"
            "- `git restore <ファイル>`（`--staged` なし）でワーキングツリーの変更を最後のコミットに戻せます。\n"
            "- `git restore --staged .` でステージ全体をアンステージできます。"
        ),
    },
    {
        "id": 24,
        "level": 3,
        "category": "ファイル操作",
        "question": "`main.py` のワーキングツリーの変更を最後のコミット状態に戻すコマンドは？（`git restore` を使ってください）",
        "answer": ["git restore main.py"],
        "hint": "ファイルを最後にコミットした状態に「復元」します。",
        "explanation": (
            "**`git restore <ファイル>`** は、ワーキングツリーのファイルをHEAD（最新コミット）の状態に戻します。\n\n"
            "- **未コミットの変更が消えるため、注意が必要です。**\n"
            "- `git restore --source=<コミットハッシュ> <ファイル>` で特定コミット時点のファイルを復元できます。\n"
            "- 旧来は `git checkout -- <ファイル>` が使われていました。"
        ),
    },
    {
        "id": 25,
        "level": 3,
        "category": "ログ",
        "question": "コミット履歴を1行（ハッシュ+メッセージ）でグラフ表示するコマンドは？",
        "answer": ["git log --oneline --graph", "git log --graph --oneline", "git log --oneline --graph --all", "git log --graph --oneline --all"],
        "hint": "`--oneline` と `--graph` を組み合わせます。",
        "explanation": (
            "**`git log --oneline --graph`** は、コミット履歴をASCIIグラフで視覚的に表示します。\n\n"
            "- `--all` を追加するとすべてのブランチ・タグを含めて表示します。\n"
            "- `--decorate` でブランチ名・タグ名も表示されます（最近のGitではデフォルトで有効）。\n"
            "- エイリアスに設定すると便利です：`git config --global alias.lg 'log --oneline --graph --all'`"
        ),
    },
    {
        "id": 26,
        "level": 3,
        "category": "ファイル操作",
        "question": "Gitの管理から `secret.txt` を削除し、ファイルもローカルから削除するコマンドは？",
        "answer": ["git rm secret.txt"],
        "hint": "追跡対象から除去するコマンドです。",
        "explanation": (
            "**`git rm <ファイル>`** は、Gitの追跡対象からファイルを削除し、ワーキングツリーからも削除します。\n\n"
            "- `git rm --cached <ファイル>` でGit管理からのみ削除し、ファイル自体はローカルに残します（`.gitignore` に追加するケースで使用）。\n"
            "- `git rm -r <ディレクトリ>` でディレクトリごと削除できます。\n"
            "- 削除もコミットで記録されます。"
        ),
    },
    {
        "id": 27,
        "level": 3,
        "category": "ファイル操作",
        "question": "`old_name.py` を `new_name.py` にリネーム（移動）するGitコマンドは？",
        "answer": ["git mv old_name.py new_name.py"],
        "hint": "`mv` コマンドのGit版です。",
        "explanation": (
            "**`git mv <旧ファイル名> <新ファイル名>`** は、ファイルのリネームをGitに認識させます。\n\n"
            "- 内部的には `mv`→`git rm`→`git add` と同等の操作です。\n"
            "- `git status` で `renamed: old_name.py -> new_name.py` と表示されます。\n"
            "- Gitはリネームを自動検出しますが、`git mv` を使うほうが明示的で確実です。"
        ),
    },
    {
        "id": 28,
        "level": 3,
        "category": "検索",
        "question": "リポジトリ内のファイルで `TODO` という文字列を含む行を検索するコマンドは？",
        "answer": ["git grep TODO"],
        "hint": "Gitが追跡するファイルを対象に `grep` するコマンドです。",
        "explanation": (
            "**`git grep <パターン>`** は、Gitが追跡するファイルの中でパターンに一致する行を検索します。\n\n"
            "- `git grep -n TODO` で行番号も表示します。\n"
            "- `git grep -l TODO` でファイル名のみ表示します。\n"
            "- `git grep TODO HEAD~3` で3つ前のコミット時点の内容を検索することもできます。\n"
            "- 通常の `grep` より高速で、追跡ファイルのみが対象なので `.gitignore` を考慮します。"
        ),
    },
    {
        "id": 29,
        "level": 3,
        "category": "設定",
        "question": "`ls` というエイリアスを `log --oneline` に設定するGitコマンドは？",
        "answer": ['git config --global alias.ls "log --oneline"', "git config --global alias.ls 'log --oneline'"],
        "hint": "`git config --global alias.<エイリアス名>` の形式を使います。",
        "explanation": (
            "**`git config --global alias.<名前> \"<コマンド>\"`** でよく使うコマンドのショートカットを作れます。\n\n"
            "- 設定後は `git ls` で `git log --oneline` が実行できます。\n"
            "- `~/.gitconfig` の `[alias]` セクションに保存されます。\n"
            "- `!` を先頭に付けるとシェルコマンドをエイリアス化できます：`alias.root = '!pwd'`"
        ),
    },
    {
        "id": 30,
        "level": 3,
        "category": "無視設定",
        "question": "`.gitignore` に追加する前にすでに追跡されているファイルをGit管理から除外し、ファイルは残すコマンドは？（例：`config/secret.env`）",
        "answer": ["git rm --cached config/secret.env"],
        "hint": "`--cached` オプションでインデックスのみから削除します。",
        "explanation": (
            "**`git rm --cached <ファイル>`** は、Gitのインデックスからファイルを削除しますが、ローカルファイルは残します。\n\n"
            "- その後 `.gitignore` に追加することで、以降は追跡されなくなります。\n"
            "- すでにコミット済みのファイルはこの操作をコミットするまで追跡が続きます。\n"
            "- ディレクトリ全体を対象にするには `git rm -r --cached <ディレクトリ>` を使います。"
        ),
    },
    # ===== Level 4: Rebase & Cherry-pick =====
    {
        "id": 31,
        "level": 4,
        "category": "リベース",
        "question": "現在のブランチを `main` ブランチの最新コミットの上にリベースするコマンドは？",
        "answer": ["git rebase main"],
        "hint": "コミットを「再適用」する操作です。",
        "explanation": (
            "**`git rebase <ブランチ>`** は、現在のブランチのコミットを指定ブランチの先端に移動させます。\n\n"
            "- マージと違い、直線的な履歴を保てます。\n"
            "- コンフリクトが発生したら解決後に `git rebase --continue`、中止は `git rebase --abort`。\n"
            "- **プッシュ済みのコミットへの `rebase` は履歴の書き換えになるため、共有ブランチでは使わないこと。**"
        ),
    },
    {
        "id": 32,
        "level": 4,
        "category": "リベース",
        "question": "直近3つのコミットをインタラクティブにリベースするコマンドは？",
        "answer": ["git rebase -i HEAD~3", "git rebase --interactive HEAD~3"],
        "hint": "`-i` オプションで対話型になります。",
        "explanation": (
            "**`git rebase -i HEAD~N`** は、直近N個のコミットをエディタで操作できます。\n\n"
            "- `pick`：そのまま適用。\n"
            "- `squash`（`s`）：直前のコミットに統合。\n"
            "- `reword`（`r`）：メッセージを書き直す。\n"
            "- `drop`（`d`）：コミットを削除。\n"
            "- `edit`（`e`）：コミット内容を修正。\n"
            "- 複数コミットをまとめる（squash）のによく使われます。"
        ),
    },
    {
        "id": 33,
        "level": 4,
        "category": "チェリーピック",
        "question": "コミット `abc1234` の変更を現在のブランチに取り込むコマンドは？",
        "answer": ["git cherry-pick abc1234"],
        "hint": "特定コミットだけを「つまみ食い」するコマンドです。",
        "explanation": (
            "**`git cherry-pick <コミットハッシュ>`** は、特定のコミットだけを現在のブランチに適用します。\n\n"
            "- 別ブランチの特定の修正だけを取り込みたいときに便利です。\n"
            "- `git cherry-pick abc1234..def5678` で範囲指定もできます。\n"
            "- コンフリクト時は解決後に `git cherry-pick --continue`。\n"
            "- `--no-commit`（`-n`）でコミットせずに変更だけを適用します。"
        ),
    },
    {
        "id": 34,
        "level": 4,
        "category": "リベース",
        "question": "リベース中にコンフリクトを解決した後、リベースを続行するコマンドは？",
        "answer": ["git rebase --continue"],
        "hint": "コンフリクト解決後にリベースを「続ける」コマンドです。",
        "explanation": (
            "**`git rebase --continue`** は、コンフリクトを解決した後にリベースを再開します。\n\n"
            "- コンフリクト解決手順：① ファイルを編集して解決 → ② `git add <ファイル>` → ③ `git rebase --continue`\n"
            "- `git rebase --skip` で現在のコミットをスキップします。\n"
            "- `git rebase --abort` でリベース前の状態に完全に戻します。"
        ),
    },
    {
        "id": 35,
        "level": 4,
        "category": "ブランチ",
        "question": "リモートの `origin/develop` を追跡するローカルブランチ `develop` を作成して切り替えるコマンドは？",
        "answer": ["git switch -c develop origin/develop", "git checkout -b develop origin/develop"],
        "hint": "リモートブランチから直接ブランチを作成して切り替えます。",
        "explanation": (
            "**`git switch -c <ローカルブランチ> <リモート追跡ブランチ>`** は、リモートブランチを元にローカルブランチを作成し、追跡関係を設定します。\n\n"
            "- 作成されたブランチは `origin/develop` を上流として追跡するため、`git pull`/`git push` が簡単になります。\n"
            "- `git branch -vv` で追跡関係を確認できます。\n"
            "- 古い書き方：`git checkout -b develop origin/develop`"
        ),
    },
    {
        "id": 36,
        "level": 4,
        "category": "差分確認",
        "question": "`main` ブランチと現在のブランチが分岐してからの差分を確認するコマンドは？",
        "answer": ["git diff main...", "git diff main...HEAD"],
        "hint": "三点ドット（`...`）を使った差分表示です。",
        "explanation": (
            "**`git diff main...`** は、`main` と現在のブランチの共通祖先から現在のブランチまでの差分を表示します。\n\n"
            "- `..`（二点）は単純な差分（2つのコミットの比較）。\n"
            "- `...`（三点）は共通祖先を基準にした差分（PRでの変更確認に適しています）。\n"
            "- `git log main...HEAD` でブランチ分岐後のコミット一覧も確認できます。"
        ),
    },
    {
        "id": 37,
        "level": 4,
        "category": "ログ",
        "question": "`src/main.py` の変更履歴を追うコマンドは？",
        "answer": ["git log src/main.py", "git log -- src/main.py"],
        "hint": "`git log` でファイルパスを指定します。",
        "explanation": (
            "**`git log <ファイルパス>`** は、特定ファイルの変更履歴のみを表示します。\n\n"
            "- `git log -p src/main.py` で各コミットの差分も一緒に表示します。\n"
            "- `git log --follow src/main.py` でリネーム前の履歴も追跡します。\n"
            "- `--` でファイルパスとコマンドオプションを区別することが推奨されます。"
        ),
    },
    {
        "id": 38,
        "level": 4,
        "category": "ログ",
        "question": "`main.py` の各行が最後に変更されたコミットと著者を表示するコマンドは？",
        "answer": ["git blame main.py"],
        "hint": "誰がその行を書いたかを「責める（blame）」コマンドです。",
        "explanation": (
            "**`git blame <ファイル>`** は、ファイルの各行について「いつ・誰が・どのコミットで」変更したかを表示します。\n\n"
            "- `git blame -L 10,20 main.py` で10〜20行目だけを表示します。\n"
            "- `git blame -w` でホワイトスペースの変更を無視します。\n"
            "- VSCodeの「Git Lens」拡張機能を使うとGUIで確認できます。"
        ),
    },
    {
        "id": 39,
        "level": 4,
        "category": "参照ログ",
        "question": "HEADの移動履歴（reflog）を表示するコマンドは？",
        "answer": ["git reflog", "git reflog show"],
        "hint": "「参照ログ」を見るコマンドです。リセットのやり直しに役立ちます。",
        "explanation": (
            "**`git reflog`** は、HEADとブランチの移動履歴をローカルに記録したログを表示します。\n\n"
            "- `git reset --hard` でコミットを消してしまっても、reflog があれば復元できます。\n"
            "- `git reset --hard HEAD@{2}` で2つ前の状態に戻せます。\n"
            "- reflog はローカルのみ（リモートには送れません）で、デフォルト90日間保持されます。"
        ),
    },
    {
        "id": 40,
        "level": 4,
        "category": "サブモジュール",
        "question": "サブモジュール `libs/helper` を `https://github.com/example/helper.git` として追加するコマンドは？",
        "answer": ["git submodule add https://github.com/example/helper.git libs/helper"],
        "hint": "`git submodule add <URL> <パス>` の形式です。",
        "explanation": (
            "**`git submodule add <URL> <パス>`** は、別のリポジトリを現在のリポジトリのサブモジュールとして追加します。\n\n"
            "- `.gitmodules` ファイルにサブモジュールの設定が記録されます。\n"
            "- クローン時にサブモジュールも取得するには `git clone --recurse-submodules <URL>` を使います。\n"
            "- `git submodule update --init --recursive` で既存リポジトリのサブモジュールを初期化・取得できます。"
        ),
    },
    # ===== Level 5: Advanced Operations =====
    {
        "id": 41,
        "level": 5,
        "category": "コンフリクト",
        "question": "マージのコンフリクトが発生したとき、自分のブランチの変更（ours）を優先して解決するコマンドは？（`main.py` に対して）",
        "answer": ["git checkout --ours main.py", "git restore --ours main.py"],
        "hint": "「自分たち（ours）」の変更を選ぶオプションです。",
        "explanation": (
            "**`git checkout --ours <ファイル>`** は、コンフリクト時に現在のブランチ（ours）の変更を採用します。\n\n"
            "- `--theirs` を使うとマージするブランチ側の変更を採用します。\n"
            "- 採用後は `git add <ファイル>` でステージしてからコミットします。\n"
            "- `git mergetool` で3方向マージツールを使いGUIで解決することもできます。"
        ),
    },
    {
        "id": 42,
        "level": 5,
        "category": "Worktree",
        "question": "同じリポジトリで別ブランチを別ディレクトリ `../hotfix` でチェックアウトするコマンドは？",
        "answer": ["git worktree add ../hotfix hotfix", "git worktree add ../hotfix"],
        "hint": "`git worktree add <パス> <ブランチ>` の形式です。",
        "explanation": (
            "**`git worktree add <パス> <ブランチ>`** は、同一リポジトリを複数のディレクトリで同時に作業できるようにします。\n\n"
            "- 1つのリポジトリで複数ブランチを同時にチェックアウトできます（`.git` を共有）。\n"
            "- `git worktree list` で一覧表示。\n"
            "- `git worktree remove <パス>` で削除。\n"
            "- 重いリポジトリでブランチを頻繁に切り替えるより高速です。"
        ),
    },
    {
        "id": 43,
        "level": 5,
        "category": "バイナリ検索",
        "question": "バグが導入されたコミットを二分探索で特定するコマンドを開始するには？",
        "answer": ["git bisect start"],
        "hint": "「二分（bisect）」探索を開始するコマンドです。",
        "explanation": (
            "**`git bisect start`** は、バグ導入コミットを効率的に特定するための二分探索を開始します。\n\n"
            "- 手順：① `git bisect start` → ② `git bisect bad`（現在がバグあり） → ③ `git bisect good <正常コミット>` → ④ 自動で中間コミットをチェックアウト → ⑤ テストして `git bisect good/bad` を繰り返す\n"
            "- `git bisect run <スクリプト>` でテストスクリプトを自動実行できます。\n"
            "- 完了後は `git bisect reset` で元に戻します。"
        ),
    },
    {
        "id": 44,
        "level": 5,
        "category": "スパースチェックアウト",
        "question": "スパースチェックアウトを有効にするコマンドは？",
        "answer": ["git sparse-checkout init", "git sparse-checkout set"],
        "hint": "巨大リポジトリの一部だけをチェックアウトする機能です。",
        "explanation": (
            "**`git sparse-checkout init`** は、スパースチェックアウト機能を有効にします。\n\n"
            "- `git sparse-checkout set src/` で `src/` ディレクトリのみをチェックアウトできます。\n"
            "- `git sparse-checkout list` で現在の設定を確認。\n"
            "- 巨大なモノレポで必要なファイルだけを扱う場合に有効です。"
        ),
    },
    {
        "id": 45,
        "level": 5,
        "category": "バンドル",
        "question": "リポジトリ全体を1ファイルにパッケージするコマンドは？（出力ファイル名: `repo.bundle`）",
        "answer": ["git bundle create repo.bundle --all"],
        "hint": "ネットワークなしでリポジトリを転送できるファイルを作ります。",
        "explanation": (
            "**`git bundle create <ファイル> --all`** は、すべてのブランチ・タグを含む単一ファイルを作成します。\n\n"
            "- `git clone repo.bundle` でバンドルファイルからクローンできます。\n"
            "- オフライン環境でのリポジトリ転送に有効です。\n"
            "- `git bundle verify repo.bundle` で整合性を確認できます。"
        ),
    },
    {
        "id": 46,
        "level": 5,
        "category": "フィルタリング",
        "question": "特定ファイル（`passwords.txt`）をリポジトリの**全履歴から**削除するコマンドは？（`git filter-repo` 使用）",
        "answer": ["git filter-repo --path passwords.txt --invert-paths"],
        "hint": "`--invert-paths` で指定パス以外を残します。",
        "explanation": (
            "**`git filter-repo --path <ファイル> --invert-paths`** は、指定ファイルをリポジトリの全履歴から削除します。\n\n"
            "- `git filter-repo` は旧来の `git filter-branch` の高速な代替ツールです（pip install git-filter-repo）。\n"
            "- 機密情報を誤ってコミットした場合に使いますが、**全員がリポジトリを再クローンする必要があります**。\n"
            "- GitHub では「BFG Repo Cleaner」も広く使われています。"
        ),
    },
    {
        "id": 47,
        "level": 5,
        "category": "プロトコル",
        "question": "SSH ではなく HTTPS でクローンする際の認証情報をキャッシュするコマンドは？（15分間）",
        "answer": ["git config --global credential.helper cache", "git config credential.helper cache"],
        "hint": "`credential.helper` を `cache` に設定します。",
        "explanation": (
            "**`git config --global credential.helper cache`** は、HTTPS認証の資格情報を一定時間メモリにキャッシュします。\n\n"
            "- デフォルトは15分。`--timeout=3600` で秒単位で変更できます。\n"
            "- `store` にするとディスクに平文保存（セキュリティリスクあり）。\n"
            "- macOS では `osxkeychain`、Windows では `manager` が推奨されます。"
        ),
    },
    {
        "id": 48,
        "level": 5,
        "category": "フック",
        "question": "コミット前に自動実行されるGitフックのファイル名は？（`.git/hooks/` 内）",
        "answer": ["pre-commit"],
        "hint": "コミット「前（pre）」に実行される「コミット（commit）」フックです。",
        "explanation": (
            "**`pre-commit`** フックは、`git commit` 実行時に最初に呼ばれるスクリプトです。\n\n"
            "- 非ゼロ終了するとコミットが中断されます。\n"
            "- リンター・テスト・フォーマットチェックを自動実行するのに使われます。\n"
            "- `pre-commit` フレームワーク（pip install pre-commit）で複数フックを管理するのが一般的です。\n"
            "- `git commit --no-verify` でフックをスキップできます（非推奨）。"
        ),
    },
    {
        "id": 49,
        "level": 5,
        "category": "サブツリー",
        "question": "サブツリーとして `https://github.com/example/lib.git` の `main` ブランチを `libs/` に追加するコマンドは？",
        "answer": ["git subtree add --prefix=libs/ https://github.com/example/lib.git main", "git subtree add --prefix libs/ https://github.com/example/lib.git main"],
        "hint": "`git subtree add --prefix=<パス> <URL> <ブランチ>` の形式です。",
        "explanation": (
            "**`git subtree add`** は、外部リポジトリをサブツリーとして組み込みます。\n\n"
            "- サブモジュールと違い、追加するリポジトリのコードが直接コピーされます（`.gitmodules` 不要）。\n"
            "- クローンするだけで完全に動作し、サブモジュールの初期化が不要です。\n"
            "- `git subtree pull --prefix=libs/ <URL> main` で更新を取り込めます。"
        ),
    },
    {
        "id": 50,
        "level": 5,
        "category": "差分確認",
        "question": "ステージングエリアとHEADの差分を表示するコマンドは？",
        "answer": ["git diff --staged", "git diff --cached"],
        "hint": "`--staged` または `--cached` オプションを使います。",
        "explanation": (
            "**`git diff --staged`** は、インデックス（ステージ）とHEADの差分を表示します。コミット前の最終確認に使います。\n\n"
            "- `--staged` と `--cached` はまったく同じオプションです。\n"
            "- `git diff`（オプションなし）はワーキングツリーとインデックスの差分。\n"
            "- `git diff HEAD` はワーキングツリーとHEADの差分（ステージ済み+未ステージ）。"
        ),
    },
    # ===== Level 6: Workflows =====
    {
        "id": 51,
        "level": 6,
        "category": "ワークフロー",
        "question": "`main` ブランチに `feature/search` をスカッシュマージするコマンドは？（現在 `main` にいる前提）",
        "answer": ["git merge --squash feature/search"],
        "hint": "`--squash` オプションで複数コミットを1つにまとめてマージします。",
        "explanation": (
            "**`git merge --squash <ブランチ>`** は、指定ブランチの変更をすべてインデックスに取り込みますが、"
            "コミットは作成しません（別途 `git commit` が必要）。\n\n"
            "- 機能ブランチの複数コミットを `main` には1つのコミットとして記録できます。\n"
            "- 履歴をシンプルに保ちたいプロジェクトで有効。\n"
            "- ただし元ブランチとの分岐関係が失われるため、以降そのブランチからマージするとコンフリクトになります。"
        ),
    },
    {
        "id": 52,
        "level": 6,
        "category": "ワークフロー",
        "question": "GitHub Flow において、機能開発後のPRマージ後にリモートの `feature/login` ブランチを削除するコマンドは？",
        "answer": ["git push origin --delete feature/login"],
        "hint": "`--delete` オプションでリモートブランチを削除します。",
        "explanation": (
            "**`git push origin --delete <ブランチ名>`** は、リモートリポジトリのブランチを削除します。\n\n"
            "- PRマージ後は不要になったブランチを削除するのがベストプラクティスです。\n"
            "- GitHub では「Delete branch」ボタンでも同じ操作ができます。\n"
            "- ローカルの追跡ブランチを削除するには `git branch -d feature/login` も必要です。\n"
            "- `git fetch --prune` でリモートに存在しないブランチの追跡情報を一括削除できます。"
        ),
    },
    {
        "id": 53,
        "level": 6,
        "category": "コミット",
        "question": "すべてのトラッキングファイルの変更をステージせずに直接コミットするコマンドは？（メッセージ: `update`）",
        "answer": ['git commit -am "update"', "git commit -am 'update'"],
        "hint": "`-a` オプションで追跡済みファイルを自動ステージします。",
        "explanation": (
            "**`git commit -am \"<メッセージ>\"`** は、追跡済みファイルの変更を自動ステージしてコミットします。\n\n"
            "- `-a` は「all」の略で、`git add` を省略できます。\n"
            "- **新規（未追跡）ファイルは含まれません。** まず `git add` が必要。\n"
            "- 手軽ですが、意図しないファイルを含めないよう `git status` で確認してから使いましょう。"
        ),
    },
    {
        "id": 54,
        "level": 6,
        "category": "タグ",
        "question": "注釈付きタグ `v2.0.0` をメッセージ `\"Release 2.0.0\"` で作成するコマンドは？",
        "answer": ['git tag -a v2.0.0 -m "Release 2.0.0"', "git tag -a v2.0.0 -m 'Release 2.0.0'"],
        "hint": "`-a` で注釈付き、`-m` でメッセージを指定します。",
        "explanation": (
            "**`git tag -a <タグ名> -m \"<メッセージ>\"`** は、著者・日時・メッセージを持つ注釈付きタグを作成します。\n\n"
            "- 軽量タグ（`git tag v2.0.0`）は単なるコミットへのポインタです。\n"
            "- 注釈付きタグは `git show v2.0.0` で詳細を確認できます。\n"
            "- リリースには注釈付きタグを使うのがベストプラクティスです。\n"
            "- `git push origin v2.0.0` でリモートにタグを送信します。"
        ),
    },
    {
        "id": 55,
        "level": 6,
        "category": "ログ",
        "question": "2024年1月1日以降のコミットのみを表示するコマンドは？",
        "answer": ['git log --after="2024-01-01"', 'git log --since="2024-01-01"'],
        "hint": "`--after` または `--since` オプションで日付フィルタリングできます。",
        "explanation": (
            "**`git log --after=\"<日付>\"`** は、指定日以降のコミットのみを表示します。\n\n"
            "- `--before`（`--until`）で指定日以前のコミットを絞り込めます。\n"
            "- `--author=\"Taro\"` で特定の作者のコミットのみ表示。\n"
            "- `--grep=\"fix\"` でコミットメッセージに `fix` を含むものを絞り込めます。\n"
            "- 複数条件を組み合わせると強力なフィルタリングができます。"
        ),
    },
    {
        "id": 56,
        "level": 6,
        "category": "メンテナンス",
        "question": "リポジトリのガベージコレクション（不要オブジェクトの削除・圧縮）を実行するコマンドは？",
        "answer": ["git gc"],
        "hint": "「ガベージコレクション（gc）」のコマンドです。",
        "explanation": (
            "**`git gc`** は、不要なオブジェクトを削除し、パックファイルを最適化することでリポジトリを圧縮します。\n\n"
            "- 通常はGitが自動実行しますが、手動で実行することもできます。\n"
            "- `git gc --aggressive` でより積極的な最適化を行います（時間がかかります）。\n"
            "- `git count-objects -v` で最適化前後のオブジェクト数を確認できます。"
        ),
    },
    {
        "id": 57,
        "level": 6,
        "category": "差分確認",
        "question": "2つのブランチ `main` と `develop` のファイル `app.py` の差分を表示するコマンドは？",
        "answer": ["git diff main develop app.py", "git diff main..develop app.py", "git diff main develop -- app.py"],
        "hint": "`git diff <ブランチ1> <ブランチ2> <ファイル>` の形式です。",
        "explanation": (
            "**`git diff <ブランチ1> <ブランチ2> <ファイル>`** は、2つのブランチ間の特定ファイルの差分を表示します。\n\n"
            "- `--` でファイルパスとブランチ名の区切りを明示できます。\n"
            "- `git diff main..develop` でブランチ間全体の差分も確認できます。\n"
            "- `git difftool` で外部ツール（VSCode、Vimdiffなど）で差分を確認できます。"
        ),
    },
    {
        "id": 58,
        "level": 6,
        "category": "フック",
        "question": "コミットメッセージが書き込まれた後に実行されるGitフックのファイル名は？",
        "answer": ["commit-msg"],
        "hint": "メッセージ（msg）がコミット（commit）された後のフックです。",
        "explanation": (
            "**`commit-msg`** フックは、コミットメッセージが保存された後に呼ばれます。\n\n"
            "- コミットメッセージのフォーマット検証（例：Conventional Commits）に使われます。\n"
            "- 非ゼロ終了でコミットが中断されます。\n"
            "- `prepare-commit-msg`：エディタ起動前（テンプレート挿入など）\n"
            "- `commit-msg`：メッセージ検証\n"
            "- `post-commit`：コミット後の通知などに使用"
        ),
    },
    {
        "id": 59,
        "level": 6,
        "category": "オブジェクト",
        "question": "コミットハッシュ `abc1234` のコミットオブジェクトの内容を表示するコマンドは？",
        "answer": ["git cat-file -p abc1234"],
        "hint": "`cat-file -p` でオブジェクトの内容を「きれいに（pretty）」表示します。",
        "explanation": (
            "**`git cat-file -p <ハッシュ>`** は、Gitオブジェクト（commit/tree/blob/tag）の内容を表示します。\n\n"
            "- `-t` でオブジェクトのタイプを確認できます。\n"
            "- コミットオブジェクトには `tree`・`parent`・`author`・`committer`・メッセージが含まれます。\n"
            "- Gitの内部構造を理解するのに役立つコマンドです。"
        ),
    },
    {
        "id": 60,
        "level": 6,
        "category": "ログ",
        "question": "コミット `abc1234` から `def5678` の間に変更されたファイル一覧を表示するコマンドは？",
        "answer": ["git diff --name-only abc1234 def5678"],
        "hint": "`--name-only` でファイル名のみ表示します。",
        "explanation": (
            "**`git diff --name-only <コミット1> <コミット2>`** は、2つのコミット間で変更されたファイル名のみを表示します。\n\n"
            "- `--name-status` で変更タイプ（M:変更、A:追加、D:削除）も表示します。\n"
            "- `--stat` で各ファイルの追加/削除行数のサマリーを表示します。\n"
            "- CIパイプラインで変更ファイルに基づく条件実行に活用できます。"
        ),
    },
    # ===== Level 7: Advanced Config & Tools =====
    {
        "id": 61,
        "level": 7,
        "category": "設定",
        "question": "Gitのデフォルトエディタを `vim` に設定するコマンドは？",
        "answer": ["git config --global core.editor vim"],
        "hint": "`core.editor` キーを使います。",
        "explanation": (
            "**`git config --global core.editor vim`** は、コミットメッセージ編集などで使うエディタを設定します。\n\n"
            "- VSCode を使う場合：`git config --global core.editor 'code --wait'`\n"
            "- nano：`git config --global core.editor nano`\n"
            "- emacs：`git config --global core.editor emacs`\n"
            "- `--wait` フラグはエディタを閉じるまでGitが待機するために必要です。"
        ),
    },
    {
        "id": 62,
        "level": 7,
        "category": "設定",
        "question": "プッシュのデフォルト動作を `current`（同名のリモートブランチにプッシュ）に設定するコマンドは？",
        "answer": ["git config --global push.default current"],
        "hint": "`push.default` を `current` に設定します。",
        "explanation": (
            "**`git config --global push.default current`** は、`git push` 時に現在のブランチと同名のリモートブランチにプッシュします。\n\n"
            "- `simple`（Git 2.0のデフォルト）：上流ブランチが設定されているときのみプッシュ。\n"
            "- `matching`：同名のリモートブランチすべてにプッシュ（古いデフォルト）。\n"
            "- `current`：同名リモートブランチへ（なければ作成）。個人開発に便利。\n"
            "- `upstream`：上流ブランチへプッシュ（ブランチ名が違っても可）。"
        ),
    },
    {
        "id": 63,
        "level": 7,
        "category": "設定",
        "question": "`git pull` のデフォルト動作を rebase にするコマンドは？",
        "answer": ["git config --global pull.rebase true"],
        "hint": "`pull.rebase` を `true` に設定します。",
        "explanation": (
            "**`git config --global pull.rebase true`** は、`git pull` 時にマージではなくリベースを使用します。\n\n"
            "- マージコミットが作られないため、履歴が直線的になります。\n"
            "- `ff-only` にすると Fast-forward のみ許可（コンフリクト時は失敗して手動対応が必要）。\n"
            "- チームの方針に合わせて設定しましょう。"
        ),
    },
    {
        "id": 64,
        "level": 7,
        "category": "差分",
        "question": "行単位ではなく単語単位で差分を表示するコマンドは？",
        "answer": ["git diff --word-diff"],
        "hint": "`--word-diff` オプションを使います。",
        "explanation": (
            "**`git diff --word-diff`** は、変更を行単位ではなく単語単位で表示します。\n\n"
            "- ドキュメントや文章の変更確認に特に有用です。\n"
            "- `--word-diff=color` でカラー表示のみ（`[- -]`・`{+ +}` なし）。\n"
            "- `--word-diff-regex=<正規表現>` で単語の区切りをカスタマイズできます。"
        ),
    },
    {
        "id": 65,
        "level": 7,
        "category": "ログ",
        "question": "特定の文字列 `bug_fix` がコードに追加・削除されたコミットを検索するコマンドは？",
        "answer": ["git log -S bug_fix", 'git log -S "bug_fix"'],
        "hint": "`-S` オプション（ピッケルアックス）で文字列の追加/削除を検索します。",
        "explanation": (
            "**`git log -S <文字列>`** は、指定文字列の出現数が変化したコミットを検索します（pickaxe オプション）。\n\n"
            "- `git log -G <正規表現>` でパターンに一致する差分を含むコミットを検索できます。\n"
            "- `-S` は文字列の「追加または削除」を検索、`-G` は差分行に正規表現マッチ。\n"
            "- `git log -S bug_fix --source --all` でブランチをまたいで検索できます。"
        ),
    },
    {
        "id": 66,
        "level": 7,
        "category": "メンテナンス",
        "question": "リポジトリ内の到達不能オブジェクトを確認するコマンドは？",
        "answer": ["git fsck"],
        "hint": "ファイルシステムチェック（fsck）のGit版です。",
        "explanation": (
            "**`git fsck`** は、Gitオブジェクトデータベースの整合性を検証し、到達不能なオブジェクトを報告します。\n\n"
            "- `git fsck --unreachable` で到達不能オブジェクトの一覧を表示。\n"
            "- `git fsck --lost-found` で失われたコミットを `.git/lost-found/` に書き出せます。\n"
            "- `git reflog` と組み合わせると、消したコミットを復元できることがあります。"
        ),
    },
    {
        "id": 67,
        "level": 7,
        "category": "設定",
        "question": "`.gitattributes` を使って `*.py` ファイルの改行コードをLFに統一する設定は？",
        "answer": ["*.py text eol=lf"],
        "hint": "`text eol=lf` でLF固定にします。",
        "explanation": (
            "**`.gitattributes` の `*.py text eol=lf`** は、`.py` ファイルのチェックアウト時の改行をLFに統一します。\n\n"
            "- `* text=auto` ですべてのテキストファイルを自動変換。\n"
            "- `*.bat text eol=crlf` でバッチファイルをCRLF固定に。\n"
            "- Windows/Mac/Linux 混在チームで改行コードの問題を防ぎます。\n"
            "- `core.autocrlf` より `.gitattributes` のほうがリポジトリレベルで管理でき推奨されます。"
        ),
    },
    {
        "id": 68,
        "level": 7,
        "category": "パッチ",
        "question": "コミット `abc1234` の変更をパッチファイル（`.patch`）として書き出すコマンドは？",
        "answer": ["git format-patch -1 abc1234"],
        "hint": "`format-patch -1` で1つのコミットをパッチ化します。",
        "explanation": (
            "**`git format-patch -1 <コミット>`** は、指定コミットの変更をメールで送れる形式のパッチファイルとして出力します。\n\n"
            "- `-n` で直近n件分のコミットをパッチ化できます。\n"
            "- `git am <パッチファイル>` でパッチを適用します。\n"
            "- オープンソースプロジェクトへのパッチ投稿にかつて広く使われていました。"
        ),
    },
    {
        "id": 69,
        "level": 7,
        "category": "注釈",
        "question": "`README.md` の各行の変更を、コミットを移動しながら追跡するコマンドは？",
        "answer": ["git blame -M README.md", "git blame --move README.md"],
        "hint": "`-M` オプションでファイル内のコードの移動を追跡します。",
        "explanation": (
            "**`git blame -M <ファイル>`** は、同じファイル内でコードが移動・コピーされた場合でも元のコミットを追跡します。\n\n"
            "- `-C` でファイル間のコードコピーも追跡します。\n"
            "- `-CC` でコミット作成時、`-CCC` でリポジトリ内の全コピーを追跡します。\n"
            "- 通常の `git blame` ではリファクタリング（コード移動）で追跡が途切れることがあります。"
        ),
    },
    {
        "id": 70,
        "level": 7,
        "category": "署名",
        "question": "GPGキーでコミットに署名するコマンドは？（メッセージ: `signed commit`）",
        "answer": ['git commit -S -m "signed commit"', "git commit -S -m 'signed commit'"],
        "hint": "`-S` オプションでGPG署名します。",
        "explanation": (
            "**`git commit -S -m \"<メッセージ>\"`** は、GPGキーでコミットに署名します。\n\n"
            "- `git config --global commit.gpgSign true` で常に署名を強制できます。\n"
            "- `git log --show-signature` で署名を確認できます。\n"
            "- GitHub の「Verified」バッジを表示するには、公開鍵をGitHubに登録する必要があります。\n"
            "- SSH署名（Git 2.34以降）も使えます：`git config --global gpg.format ssh`"
        ),
    },
    # ===== Level 8: Internals =====
    {
        "id": 71,
        "level": 8,
        "category": "内部構造",
        "question": "ワーキングツリーのファイル内容からblobオブジェクトのハッシュを計算するコマンドは？（`main.py` を対象に）",
        "answer": ["git hash-object main.py"],
        "hint": "`hash-object` でオブジェクトのハッシュを計算します。",
        "explanation": (
            "**`git hash-object <ファイル>`** は、ファイルのコンテンツからSHA-1（または SHA-256）ハッシュを計算します。\n\n"
            "- `-w` オプションを付けるとオブジェクトをGitのオブジェクトデータベースにも書き込みます。\n"
            "- Gitはファイルの中身をblobオブジェクトとしてハッシュで管理します。\n"
            "- `git cat-file -p <ハッシュ>` で内容を確認できます。"
        ),
    },
    {
        "id": 72,
        "level": 8,
        "category": "内部構造",
        "question": "現在のインデックス（ステージングエリア）の内容を一覧表示するコマンドは？",
        "answer": ["git ls-files", "git ls-files --stage"],
        "hint": "`ls-files` でインデックスのファイル一覧を表示します。",
        "explanation": (
            "**`git ls-files`** は、インデックスに登録されているファイルの一覧を表示します。\n\n"
            "- `git ls-files --others` で未追跡ファイル一覧を表示。\n"
            "- `git ls-files --deleted` で削除済みファイルを表示。\n"
            "- `git ls-files --stage` でステージングエリアの詳細（モード・ハッシュ・ファイル名）を表示。\n"
            "- `git ls-tree HEAD` でコミット時点のツリーを表示することもできます。"
        ),
    },
    {
        "id": 73,
        "level": 8,
        "category": "内部構造",
        "question": "Gitのpack ファイルのインデックスを検証するコマンドは？",
        "answer": ["git verify-pack -v .git/objects/pack/*.idx"],
        "hint": "`verify-pack` でパックファイルを検証します。",
        "explanation": (
            "**`git verify-pack -v <.idxファイル>`** は、パックファイルの整合性を検証し、内容を表示します。\n\n"
            "- Gitは多くのオブジェクトを効率的に保存するためにパックファイルを使います。\n"
            "- `git gc` でオブジェクトがパックファイルにまとめられます。\n"
            "- `git count-objects -v` でルーズオブジェクトとパック済みオブジェクトの数を確認できます。"
        ),
    },
    {
        "id": 74,
        "level": 8,
        "category": "内部構造",
        "question": "HEADが指している現在のコミットハッシュを表示するコマンドは？",
        "answer": ["git rev-parse HEAD"],
        "hint": "`rev-parse` でシンボリック参照をハッシュに変換します。",
        "explanation": (
            "**`git rev-parse HEAD`** は、HEADが指すコミットの完全なSHAハッシュを表示します。\n\n"
            "- `git rev-parse --short HEAD` で短縮ハッシュを表示します。\n"
            "- `git rev-parse --abbrev-ref HEAD` で現在のブランチ名を表示します。\n"
            "- スクリプトやCI/CDでコミットハッシュを取得するのに便利です。"
        ),
    },
    {
        "id": 75,
        "level": 8,
        "category": "内部構造",
        "question": "`main` ブランチの最新コミットのtreeオブジェクトのハッシュを表示するコマンドは？",
        "answer": ["git rev-parse main^{tree}", "git rev-parse main^\\{tree\\}"],
        "hint": "`^{tree}` でコミットのツリーオブジェクトを参照します。",
        "explanation": (
            "**`git rev-parse <コミット>^{tree}`** は、コミットが参照するツリーオブジェクトのハッシュを表示します。\n\n"
            "- `^{commit}`・`^{tag}`・`^{blob}` で型を指定して参照できます。\n"
            "- ツリーオブジェクトはディレクトリ構造を表し、blobとサブツリーへの参照を持ちます。\n"
            "- `git ls-tree <ツリーハッシュ>` でツリーの内容を確認できます。"
        ),
    },
    {
        "id": 76,
        "level": 8,
        "category": "内部構造",
        "question": "Gitオブジェクトのタイプを確認するコマンドは？（`abc1234` を対象に）",
        "answer": ["git cat-file -t abc1234"],
        "hint": "`-t` でタイプを表示します。",
        "explanation": (
            "**`git cat-file -t <ハッシュ>`** は、Gitオブジェクトのタイプを表示します。\n\n"
            "- 返される値は `commit`・`tree`・`blob`・`tag` のいずれかです。\n"
            "- `commit`：スナップショットのメタデータ\n"
            "- `tree`：ディレクトリ構造\n"
            "- `blob`：ファイルの内容\n"
            "- `tag`：注釈付きタグのオブジェクト"
        ),
    },
    {
        "id": 77,
        "level": 8,
        "category": "内部構造",
        "question": "インデックスをtreeオブジェクトとして書き込み、そのハッシュを返すコマンドは？",
        "answer": ["git write-tree"],
        "hint": "インデックスをtreeオブジェクトに変換する低レベルコマンドです。",
        "explanation": (
            "**`git write-tree`** は、現在のインデックス（ステージングエリア）をtreeオブジェクトとしてオブジェクトデータベースに書き込み、そのSHAを返します。\n\n"
            "- `git commit-tree <tree> -m \"msg\"` でtreeからコミットオブジェクトを作れます。\n"
            "- これらは `git commit` の内部で実行される低レベルコマンド（plumbing）です。\n"
            "- Gitの仕組みを深く理解するための学習に有用です。"
        ),
    },
    {
        "id": 78,
        "level": 8,
        "category": "設定",
        "question": "`.git/config` にある `[core]` セクションの `fileMode` の値を確認するコマンドは？",
        "answer": ["git config core.fileMode", "git config --local core.fileMode"],
        "hint": "`git config <セクション>.<キー>` で設定値を取得します。",
        "explanation": (
            "**`git config <キー>`** は、指定した設定キーの値を表示します。\n\n"
            "- `git config --list` ですべての設定を一覧表示します。\n"
            "- `git config --list --show-origin` で設定ファイルのパスも表示します。\n"
            "- `core.fileMode=false` は Windows の実行権限変更を無視するのに使います。"
        ),
    },
    {
        "id": 79,
        "level": 8,
        "category": "内部構造",
        "question": "`HEAD` が間接参照しているブランチ名を表示するコマンドは？",
        "answer": ["git symbolic-ref HEAD"],
        "hint": "`symbolic-ref` でシンボリック参照を読み書きします。",
        "explanation": (
            "**`git symbolic-ref HEAD`** は、HEADが指すブランチ参照（例：`refs/heads/main`）を表示します。\n\n"
            "- detached HEAD 状態（ブランチでなくコミットを直接指す）だとエラーになります。\n"
            "- `git symbolic-ref --short HEAD` でブランチ名のみ（`main` など）を表示します。\n"
            "- スクリプトで現在のブランチ名を取得するときに `git rev-parse --abbrev-ref HEAD` とともによく使われます。"
        ),
    },
    {
        "id": 80,
        "level": 8,
        "category": "内部構造",
        "question": "Gitが追跡しているすべての参照（ブランチ・タグ等）を一覧表示するコマンドは？",
        "answer": ["git show-ref"],
        "hint": "`show-ref` で参照一覧を表示します。",
        "explanation": (
            "**`git show-ref`** は、`refs/` 以下のすべての参照とそのSHAを表示します。\n\n"
            "- `git show-ref --heads` でブランチのみ。\n"
            "- `git show-ref --tags` でタグのみ。\n"
            "- `git for-each-ref` でより柔軟なフォーマット出力が可能です。\n"
            "- Gitの参照システムを理解するための学習に有用です。"
        ),
    },
    # ===== Level 9: CI/CD & GitHub Specific =====
    {
        "id": 81,
        "level": 9,
        "category": "CI/CD",
        "question": "GitHub Actions で、PRのベースブランチに対する差分ファイルを取得するコマンドは？",
        "answer": ["git diff --name-only origin/main...HEAD", "git diff --name-only origin/main..HEAD"],
        "hint": "`origin/main...HEAD` で差分のあるファイルを取得します。",
        "explanation": (
            "**`git diff --name-only origin/main...HEAD`** は、mainからの分岐以降に変更されたファイルの一覧を取得します。\n\n"
            "- GitHub Actions の `on: pull_request` では、PRのベースブランチと現在のHEADを比較するのによく使われます。\n"
            "- 変更されたファイルに基づいて特定のジョブだけを実行する（パスフィルタ）ことが可能です。\n"
            "- `git diff --stat origin/main...HEAD` で変更の統計情報も取得できます。"
        ),
    },
    {
        "id": 82,
        "level": 9,
        "category": "CI/CD",
        "question": "GitHub Actions で浅いクローン（最新1コミットのみ）をするコマンドは？",
        "answer": ["git clone --depth 1 <URL>", "git clone --depth=1 <URL>"],
        "hint": "`--depth` オプションで履歴の深さを制限します。",
        "explanation": (
            "**`git clone --depth 1 <URL>`** は、最新の1コミットのみを取得する浅いクローンを行います。\n\n"
            "- CI/CDパイプラインでの高速化に有効です（履歴不要な場合）。\n"
            "- `actions/checkout@v4` の `fetch-depth: 1` で同様の設定ができます。\n"
            "- 深い履歴が必要な場合（`git describe`・`git log` 等）は `fetch-depth: 0` で全履歴を取得します。"
        ),
    },
    {
        "id": 83,
        "level": 9,
        "category": "CI/CD",
        "question": "タグ `v1.0.0` がプッシュされたときのイベントをトリガーにするGitHub Actionsの設定は？",
        "answer": ["on:\n  push:\n    tags:\n      - 'v*'", "on:\n  push:\n    tags:\n      - 'v1.0.0'"],
        "hint": "`on: push: tags:` でタグプッシュをトリガーにします。",
        "explanation": (
            "**GitHub Actions の `on: push: tags: - 'v*'`** は、`v` で始まるタグのプッシュ時にワークフローをトリガーします。\n\n"
            "- `v*.*.*` のようにSemVer形式に限定することもできます。\n"
            "- リリースタグのプッシュ時に自動でビルド・デプロイするのが一般的なパターンです。\n"
            "- `on: release: types: [published]` でGitHubのリリース公開時にトリガーする方法もあります。"
        ),
    },
    {
        "id": 84,
        "level": 9,
        "category": "Git Large File Storage",
        "question": "Git LFSで `*.psd` ファイルを追跡対象にするコマンドは？",
        "answer": ["git lfs track '*.psd'", 'git lfs track "*.psd"'],
        "hint": "`git lfs track` でLFS管理対象を指定します。",
        "explanation": (
            "**`git lfs track '*.psd'`** は、`.psd` ファイルをGit LFS（Large File Storage）で管理するように設定します。\n\n"
            "- 設定は `.gitattributes` に書き込まれます：`*.psd filter=lfs diff=lfs merge=lfs -text`\n"
            "- `git lfs install` でLFSを初期化してから使います。\n"
            "- 動画・画像・バイナリファイルなど大きなファイルをGitHubに保存するのに有効です。\n"
            "- `git lfs ls-files` でLFS管理ファイルの一覧を確認できます。"
        ),
    },
    {
        "id": 85,
        "level": 9,
        "category": "GitHub",
        "question": "GitHub CLI (`gh`) でPRを作成するコマンドの基本形は？",
        "answer": ["gh pr create", "gh pr create --title '' --body ''"],
        "hint": "`gh pr create` がベースのコマンドです。",
        "explanation": (
            "**`gh pr create`** は、現在のブランチからGitHub上にプルリクエストを作成します。\n\n"
            "- `--title`・`--body` でタイトルと本文を指定できます。\n"
            "- `--draft` でドラフトPRとして作成できます。\n"
            "- `--assignee @me` で自分をアサインできます。\n"
            "- `--base main` でベースブランチを指定できます。"
        ),
    },
    {
        "id": 86,
        "level": 9,
        "category": "GitHub",
        "question": "GitHub CLI でIssue #42 をクローズするコマンドは？",
        "answer": ["gh issue close 42"],
        "hint": "`gh issue close <番号>` の形式です。",
        "explanation": (
            "**`gh issue close 42`** は、GitHub CLI を使ってIssue #42 をクローズします。\n\n"
            "- `gh issue create` で新しいIssueを作成。\n"
            "- `gh issue list` でIssue一覧を表示。\n"
            "- `gh issue view 42` でIssueの詳細を確認。\n"
            "- `--comment` オプションでコメントを追加しながらクローズできます。"
        ),
    },
    {
        "id": 87,
        "level": 9,
        "category": "CI/CD",
        "question": "Git のコミットメッセージで `Fixes #42` と書くとPRマージ時に何が起こるか？（GitHub の動作）",
        "answer": ["Issue #42 が自動的にクローズされる", "Issue 42 がクローズされる", "#42 がクローズされる"],
        "hint": "GitHubの自動クローズ機能です。",
        "explanation": (
            "GitHubでは、コミットメッセージや PR の説明に **`Fixes #<番号>`** などのキーワードを含めると、"
            "デフォルトブランチへのマージ時に対応するIssueが**自動的にクローズ**されます。\n\n"
            "- 使用できるキーワード：`close`・`closes`・`closed`・`fix`・`fixes`・`fixed`・`resolve`・`resolves`・`resolved`\n"
            "- 例：`Closes #42`, `Fixes #42 and #43`\n"
            "- `OWNER/REPO#42` の形式でクロスリポジトリのIssueも参照できます。"
        ),
    },
    {
        "id": 88,
        "level": 9,
        "category": "CI/CD",
        "question": "GitHub Actions で secrets の値を環境変数 `API_KEY` として参照する YAML 記法は？",
        "answer": ["${{ secrets.API_KEY }}", "env:\n  API_KEY: ${{ secrets.API_KEY }}"],
        "hint": "`${{ secrets.<名前> }}` の形式です。",
        "explanation": (
            "**`${{ secrets.API_KEY }}`** は、GitHub Actions の式構文でリポジトリのシークレットを参照します。\n\n"
            "- シークレットはリポジトリの Settings → Secrets and variables → Actions で設定します。\n"
            "- 環境変数として渡すには：`env: API_KEY: ${{ secrets.API_KEY }}`\n"
            "- ログにシークレットの値は `***` でマスクされます。\n"
            "- Organization レベルや Environment レベルのシークレットも設定できます。"
        ),
    },
    {
        "id": 89,
        "level": 9,
        "category": "GitHub",
        "question": "リポジトリの CODEOWNERS ファイルで `src/` ディレクトリのオーナーを `@team-backend` に設定する記法は？",
        "answer": ["src/ @team-backend"],
        "hint": "`<パス> <オーナー>` の形式です。",
        "explanation": (
            "**`src/ @team-backend`** は、`src/` 以下のファイル変更を含むPRに `@team-backend` チームの承認を必須にします。\n\n"
            "- `CODEOWNERS` は `.github/`・リポジトリルート・`docs/` のいずれかに配置します。\n"
            "- `*.js @frontend-team` でファイルパターンでも指定できます。\n"
            "- ブランチ保護と組み合わせることで、コードレビューの強制が可能です。\n"
            "- `@username` で個人、`@org/team` でチームを指定します。"
        ),
    },
    {
        "id": 90,
        "level": 9,
        "category": "セキュリティ",
        "question": "機密情報をコミットしてしまった際、リポジトリ全履歴からそのファイルを消去するツールのコマンドは？（BFG Repo Cleaner を使用して `secret.txt` を削除）",
        "answer": ["bfg --delete-files secret.txt"],
        "hint": "`bfg --delete-files <ファイル名>` の形式です。",
        "explanation": (
            "**`bfg --delete-files secret.txt`** は、BFG Repo Cleaner を使ってリポジトリの全履歴から `secret.txt` を削除します。\n\n"
            "- `git filter-repo` より高速で使いやすいとされています。\n"
            "- 実行後は `git reflog expire --expire=now --all && git gc --prune=now --aggressive` でオブジェクトを完全に削除します。\n"
            "- 全員がリポジトリを再クローンする必要があります。\n"
            "- 機密情報が漏れた場合は、必ずローテーション（キー/パスワードの変更）も行ってください。"
        ),
    },
    # ===== Level 10: Expert =====
    {
        "id": 91,
        "level": 10,
        "category": "内部プロトコル",
        "question": "Gitのsmart HTTPプロトコルでリモートのブランチ一覧を取得するコマンドは？",
        "answer": ["git ls-remote", "git ls-remote origin"],
        "hint": "`ls-remote` でリモートの参照一覧を取得します。",
        "explanation": (
            "**`git ls-remote`** は、リモートリポジトリの参照（ブランチ・タグ）とそのSHAを取得します。\n\n"
            "- `git ls-remote --heads origin` でブランチのみ。\n"
            "- `git ls-remote --tags origin` でタグのみ。\n"
            "- `git fetch` 前にリモートの状態を確認するのに使えます。\n"
            "- CIで特定のタグやブランチの存在確認にも使えます。"
        ),
    },
    {
        "id": 92,
        "level": 10,
        "category": "マージ戦略",
        "question": "octopusマージ（3つ以上のブランチを一度にマージ）を使って `branch1` `branch2` `branch3` をマージするコマンドは？",
        "answer": ["git merge branch1 branch2 branch3"],
        "hint": "`git merge` に複数のブランチを指定するとoctopusマージになります。",
        "explanation": (
            "**`git merge branch1 branch2 branch3`** は、複数ブランチを同時に1つのマージコミットにまとめます（octopusマージ）。\n\n"
            "- Linuxカーネルのような大規模プロジェクトで使われることがあります。\n"
            "- コンフリクトがある場合は通常マージに自動的にフォールバックします。\n"
            "- `git merge -s octopus` でマージ戦略を明示的に指定することもできます。"
        ),
    },
    {
        "id": 93,
        "level": 10,
        "category": "カスタムマージ",
        "question": "`recursive` 戦略を使い、差分アルゴリズムを `patience` に指定してマージするコマンドは？",
        "answer": ["git merge -s recursive -X diff-algorithm=patience feature", "git merge --strategy=recursive --strategy-option=diff-algorithm=patience feature"],
        "hint": "`-s` で戦略、`-X` で戦略オプションを指定します。",
        "explanation": (
            "**`git merge -s recursive -X diff-algorithm=patience`** は、patience アルゴリズムを使った差分計算でマージします。\n\n"
            "- `patience` アルゴリズムは、一意な行を基準にして差分を計算し、より読みやすい差分を生成します。\n"
            "- `-X ours`・`-X theirs` でコンフリクト時の自動解決ポリシーを設定できます。\n"
            "- `histogram` アルゴリズムも高品質な差分生成で使われます。"
        ),
    },
    {
        "id": 94,
        "level": 10,
        "category": "内部構造",
        "question": "Gitのネットワークプロトコルのバージョン2（protocol v2）を有効にするコマンドは？",
        "answer": ["git config --global protocol.version 2"],
        "hint": "`protocol.version` を `2` に設定します。",
        "explanation": (
            "**`git config --global protocol.version 2`** は、Git Wire Protocol Version 2を有効にします。\n\n"
            "- Protocol v2 は、フェッチ時のブランチフィルタリングが可能になり、大規模リポジトリでの通信が大幅に高速化されます。\n"
            "- Git 2.26以降ではデフォルトで有効になっています。\n"
            "- `GIT_TRACE_PACKET=1` でプロトコルの通信を確認できます。"
        ),
    },
    {
        "id": 95,
        "level": 10,
        "category": "マルチパック",
        "question": "Git 2.31以降で導入された、マルチパックインデックスを生成するコマンドは？",
        "answer": ["git multi-pack-index write"],
        "hint": "`multi-pack-index` コマンドを使います。",
        "explanation": (
            "**`git multi-pack-index write`** は、複数のパックファイルをまたいだ単一のインデックスを生成します。\n\n"
            "- `git gc` の代わりにパックファイルをまとめずにインデックスだけ最適化できます。\n"
            "- `git multi-pack-index verify` で整合性検証。\n"
            "- 巨大リポジトリ（Microsoft、Google スケール）での `git gc` の代替として開発されました。\n"
            "- `core.multiPackIndex = true` で自動使用が有効になります。"
        ),
    },
    {
        "id": 96,
        "level": 10,
        "category": "部分クローン",
        "question": "blobを含まず、コミットとツリーのみを取得する部分クローン（blobless clone）を実行するコマンドは？",
        "answer": ["git clone --filter=blob:none <URL>"],
        "hint": "`--filter=blob:none` でblobをスキップします。",
        "explanation": (
            "**`git clone --filter=blob:none <URL>`** は、コミット・ツリーオブジェクトのみを取得し、blobは必要なときに遅延取得します。\n\n"
            "- クローン時間と容量を大幅に削減できます。\n"
            "- `--filter=tree:0` でコミットのみを取得するtreeless cloneも可能です。\n"
            "- GitHub Sparse Checkout と組み合わせると、必要なファイルだけを必要なときに取得できます。\n"
            "- Git 2.28以降のサーバー側サポートが必要です。"
        ),
    },
    {
        "id": 97,
        "level": 10,
        "category": "再発生可能ビルド",
        "question": "コミット日時をソースからビルドへ伝達するため、HEADのコミット日時を取得するコマンドは？",
        "answer": ["git log -1 --format=%ct", "git log -1 --pretty=format:%ct"],
        "hint": "`%ct` はコミット日時のUNIXタイムスタンプです。",
        "explanation": (
            "**`git log -1 --format=%ct`** は、最新コミットのUNIXタイムスタンプを出力します。\n\n"
            "- `%ci` でISO 8601形式、`%cd` で人間が読める形式の日時を取得できます。\n"
            "- 再現可能ビルド（Reproducible Builds）では、`SOURCE_DATE_EPOCH` としてこの値を使い、ビルド成果物のタイムスタンプを固定します。\n"
            "- `git log -1 --format=%H` で最新コミットのフルハッシュを取得できます。"
        ),
    },
    {
        "id": 98,
        "level": 10,
        "category": "モノレポ",
        "question": "Git Sparse Checkout でコーンモード（cone mode）を使い `src/frontend/` のみをチェックアウトするコマンドは？",
        "answer": ["git sparse-checkout set --cone src/frontend", "git sparse-checkout set src/frontend"],
        "hint": "`git sparse-checkout set` でパスを指定します。",
        "explanation": (
            "**`git sparse-checkout set --cone src/frontend`** は、コーンモードで `src/frontend/` 以下のファイルのみをチェックアウトします。\n\n"
            "- コーンモードはディレクトリ単位での指定のみで、ファイルマッチングより高速です。\n"
            "- `git sparse-checkout list` で現在の設定確認。\n"
            "- `git sparse-checkout disable` でスパースチェックアウトを無効化。\n"
            "- Microsoftの Windows リポジトリなど超大規模モノレポで重要な機能です。"
        ),
    },
    {
        "id": 99,
        "level": 10,
        "category": "セキュリティ",
        "question": "Gitの安全なディレクトリ設定で `/workspace` をグローバルに信頼するコマンドは？",
        "answer": ["git config --global --add safe.directory /workspace"],
        "hint": "`safe.directory` にパスを追加します。",
        "explanation": (
            "**`git config --global --add safe.directory /workspace`** は、所有者が異なるディレクトリをGitが安全と判断するように設定します。\n\n"
            "- CVE-2022-24765 の対策として Git 2.35.2 で導入されました。\n"
            "- Dockerコンテナ内でルートが所有するディレクトリを別ユーザーが操作する場合などに必要です。\n"
            "- GitHub Actions でも同様のエラーが出ることがあり、`actions/checkout` の最新版で自動対応されています。\n"
            "- `*` を指定するとすべてのディレクトリを信頼しますが、セキュリティリスクがあります。"
        ),
    },
    {
        "id": 100,
        "level": 10,
        "category": "SHA-256移行",
        "question": "SHA-256ハッシュを使用する新しいGitリポジトリを初期化するコマンドは？",
        "answer": ["git init --object-format=sha256"],
        "hint": "`--object-format` オプションでハッシュアルゴリズムを指定します。",
        "explanation": (
            "**`git init --object-format=sha256`** は、従来のSHA-1の代わりにSHA-256を使用するリポジトリを作成します。\n\n"
            "- SHA-1の衝突攻撃（SHAttered）への対策として開発されました。\n"
            "- Git 2.29以降で実験的サポート、2.42以降で本格サポートが進んでいます。\n"
            "- SHA-1とSHA-256のリポジトリは**互換性がありません**（相互クローン不可）。\n"
            "- GitHubはSHA-256リポジトリのサポートを段階的に進めています。"
        ),
    },
]
