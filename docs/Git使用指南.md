# Git 使用指南

## 📋 已配置的Git文件

项目根目录下已创建以下Git配置文件：

### 1. `.gitignore`
指定不需要提交到Git的文件类型和目录。

**主要排除内容**：
- Python虚拟环境 (`venv/`, `env/`)
- Node.js依赖 (`node_modules/`)
- 环境变量文件 (`.env`, `.env.local`)
- IDE配置文件 (`.idea/`, `.vscode/`)
- 操作系统文件 (`.DS_Store`, `Thumbs.db`)
- 日志文件 (`*.log`, `logs/`)
- 数据库文件 (`*.db`, `*.sqlite`)
- 构建产物 (`dist/`, `build/`)
- 临时文件 (`*.tmp`, `*.cache`)

### 2. `.gitattributes`
配置Git如何处理不同类型的文件。

**主要配置**：
- 源代码使用LF换行符
- Windows脚本使用CRLF换行符
- 图片、字体等二进制文件标记为binary
- 锁文件(package-lock.json)不被修改

### 3. `.vscode/settings.json`
VSCode工作区配置。

**主要配置**：
- 保存时自动格式化
- Python使用black格式化
- 启用flake8代码检查
- pytest测试框架集成
- 排除不需要搜索的目录

### 4. `.vscode/extensions.json`
推荐的VSCode扩展列表。

**推荐扩展**：
- Python扩展包
- ESLint/Prettier
- TypeScript/JavaScript
- Docker
- GitLens
- Material Icon Theme

---

## 🚀 初次提交到GitHub

### 1. 初始化Git仓库

```bash
# 进入项目目录
cd D:\web\project\solararc-pro

# 初始化Git（如果还没有初始化）
git init

# 查看当前状态
git status
```

### 2. 添加所有文件到暂存区

```bash
# 添加所有文件（.gitignore会自动排除不需要的文件）
git add .

# 或者分步添加
git add backend/
git add frontend/
git add docs/
git add .gitignore .vscode/ .gitattributes
git add *.md *.yml docker-compose.yml
```

### 3. 提交更改

```bash
# 首次提交
git commit -m "Initial commit: SolarArc Pro project setup

- Backend: FastAPI + SQLAlchemy + pvlib
- Frontend: React 18 + TypeScript + Vite
- Services: Solar position, shadow calculation
- Database: MySQL with spatial indexing
- Deployment: Docker + Zeabur configuration
- Documentation: Complete design docs and guides

Co-Authored-By: Claude Sonnet <noreply@anthropic.com>"
```

### 4. 创建GitHub仓库

1. 访问 [GitHub](https://github.com/new)
2. 创建新仓库：
   - Repository name: `solararc-pro`
   - Description: 高性能城市时空日照分析与视觉仿真平台
   - Public/Private: 根据需要选择
   - ⚠️ **不要**勾选 "Add a README file"（我们已有）
   - ⚠️ **不要**勾选 "Add .gitignore"（我们已有）
3. 点击 "Create repository"

### 5. 关联远程仓库并推送

```bash
# 添加远程仓库（替换为你的用户名）
git remote add origin https://github.com/yourusername/solararc-pro.git

# 验证远程仓库
git remote -v

# 推送到GitHub（首次推送）
git branch -M main
git push -u origin main
```

或者使用SSH（推荐）：
```bash
git remote add origin git@github.com:yourusername/solararc-pro.git
git push -u origin main
```

---

## 📝 日常使用Git

### 查看状态

```bash
# 查看当前修改状态
git status

# 查看具体修改内容
git diff

# 查看已暂存的修改
git diff --staged
```

### 提交更改

```bash
# 1. 查看修改了哪些文件
git status

# 2. 添加修改的文件
# 添加所有修改
git add .

# 或添加特定文件
git add backend/app/main.py
git add frontend/src/App.tsx

# 3. 提交（写清楚提交信息）
git commit -m "feat: 添加建筑阴影计算功能

- 实现Shadow Volume算法
- 支持复杂多边形阴影
- 添加阴影缓存机制"

# 4. 推送到GitHub
git push
```

### 提交信息规范

使用约定式提交（Conventional Commits）格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型 (type)**:
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链相关

**示例**:
```bash
git commit -m "feat(solar): 添加24小时太阳位置批量计算

- 使用pvlib计算整点太阳位置
- 返回24小时数据数组
- 添加缓存优化"

git commit -m "fix(shadow): 修正阴影计算中的坐标系错误

- 纠正WGS84和GCJ-02混淆
- 更新坐标转换函数
- 修复测试用例"

git commit -m "docs: 更新README安装指南

- 添加Windows安装步骤
- 补充常见问题解答
- 更新依赖版本"
```

### 撤销更改

```bash
# 撤销工作区的修改（危险！）
git checkout -- filename.py

# 撤销暂存区的修改（保留在工作区）
git reset HEAD filename.py

# 撤销最近的提交（保留修改）
git reset --soft HEAD~1

# 撤销最近的提交（丢弃修改）
git reset --hard HEAD~1

# 恢复某个文件到指定提交状态
git checkout commit-hash -- filename.py
```

---

## 🔐 敏感信息处理

### 环境变量文件

⚠️ **重要**: `.env` 文件已在 `.gitignore` 中，不会被提交。

**但如果已误提交，需要删除**：

```bash
# 从Git历史中删除敏感文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送
git push origin --force --all
```

### 检查是否包含敏感信息

```bash
# 搜索可能的敏感信息
git grep -i "password\|secret\|api_key\|token"

# 或使用工具
git secrets --install
git secrets --scan
```

---

## 🌿 分支管理

### 创建新分支

```bash
# 创建并切换到新分支
git checkout -b feature/shadow-calculation

# 或者分两步
git branch feature/shadow-calculation
git checkout feature/shadow-calculation
```

### 合并分支

```bash
# 1. 切换到main分支
git checkout main

# 2. 拉取最新代码
git pull origin main

# 3. 合并特性分支
git merge feature/shadow-calculation

# 4. 推送合并结果
git push origin main

# 5. 删除已合并的分支（可选）
git branch -d feature/shadow-calculation
git push origin --delete feature/shadow-calculation
```

### Pull Request工作流

1. **在GitHub上创建Pull Request**
   - 访问仓库页面
   - 点击 "Pull requests" → "New pull request"
   - 选择源分支和目标分支
   - 填写PR描述
   - 点击 "Create pull request"

2. **Code Review**
   - 等待审核
   - 根据反馈修改代码
   - 更新PR（git push会自动更新PR）

3. **合并PR**
   - 审核通过后，点击 "Merge pull request"
   - 选择合并方式（Merge commit / Squash and merge）
   - 删除分支

---

## 🏷️ 标签管理

### 创建标签

```bash
# 创建轻量标签
git tag v1.0.0

# 创建附注标签（推荐）
git tag -a v1.0.0 -m "Release version 1.0.0

主要功能:
- 太阳位置计算
- 阴影计算
- 日照分析
- 3D可视化"

# 查看标签
git tag
git show v1.0.0
```

### 推送标签

```bash
# 推送特定标签
git push origin v1.0.0

# 推送所有标签
git push origin --tags
```

### 删除标签

```bash
# 删除本地标签
git tag -d v1.0.0

# 删除远程标签
git push origin --delete v1.0.0
```

---

## 📊 查看历史

### 查看提交历史

```bash
# 查看提交历史
git log

# 美化显示
git log --oneline --graph --all --decorate

# 查看最近10条
git log -10 --oneline

# 查看某个文件的修改历史
git log --follow filename.py
```

### 查看文件差异

```bash
# 比较两个分支
git diff main..develop

# 比较两个提交
git diff commit1..commit2

# 查看某个文件的修改
git diff main -- backend/app/main.py
```

---

## 🔄 同步远程仓库

### 拉取最新代码

```bash
# 拉取并合并
git pull origin main

# 或分两步（更安全）
git fetch origin
git merge origin/main
```

### 处理冲突

```bash
# 1. 拉取时发现冲突
git pull origin main

# 2. 打开冲突文件，查找 <<<<<<<标记
#手动编辑解决冲突

# 3. 标记为已解决
git add conflicted_file.py

# 4. 完成合并
git commit

# 5. 推送
git push origin main
```

---

## 🛠️ 有用的Git命令

### 别名设置

```bash
# 设置常用别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --pretty=format:"%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset" --abbrev-commit'

# 使用
git st          # git status
git co main     # git checkout main
git ci "message" # git commit -m "message"
```

### 忽略已跟踪的文件

```bash
# 停止跟踪某个文件（但保留在本地）
git rm --cached filename.py

# 停止跟踪某个目录
git rm -r --cached directory/

# 提交更改
git commit -m "chore: stop tracking filename.py"
```

### 储藏工作

```bash
# 临时保存当前工作（不提交）
git stash

# 查看储藏列表
git stash list

# 恢复储藏
git stash pop

# 恢复指定储藏
git stash apply stash@{1}

# 删除储藏
git stash drop
```

---

## 📌 最佳实践

### 1. 提交前检查

```bash
# 1. 查看修改了什么
git status

# 2. 查看具体改动
git diff

# 3. 运行测试（如果有）
# pytest backend/tests/

# 4. 添加文件
git add .

# 5. 提交
git commit -m "..."
```

### 2. 小步提交

```bash
# 好的做法：一个功能一个提交
git add backend/app/services/solar_service.py
git commit -m "feat: 添加太阳位置计算服务"

git add backend/api/v1/endpoints/solar.py
git commit -m "feat: 添加太阳位置API端点"

# 避免：一次性提交所有修改
git add .
git commit -m "完成太阳位置功能"
```

### 3. 提交信息清晰

```bash
# 好的提交信息
git commit -m "fix(shadow): 修正阴影计算中的坐标系转换错误

- 纠正GCJ-02到WGS84的转换公式
- 添加单元测试验证转换结果
- 修复issue #123"

# 不好的提交信息
git commit -m "update"
git commit -m "fix bug"
git commit -m "modify files"
```

### 4. 定期推送

```bash
# 每完成一个功能就推送
git push origin feature-branch

# 每天下班前推送
git push origin main
```

### 5. 使用.gitignore

```bash
# 定期检查.gitignore是否完整
git status

# 如果看到不应该提交的文件
# 添加到.gitignore
echo "*.log" >> .gitignore

# 移除已跟踪的文件
git rm --cached *.log
git commit -m "chore: update .gitignore"
```

---

## 🆘 常见问题

### 问题1: .gitignore不生效

**原因**: 文件已经被Git跟踪

**解决**:
```bash
# 清除缓存
git rm -r --cached .

# 重新添加
git add .
git commit -m "chore: fix .gitignore"
```

### 问题2: 推送被拒绝

**原因**: 远程有新的提交

**解决**:
```bash
# 先拉取
git pull origin main

# 如果有冲突，解决冲突后
git add .
git commit
git push origin main
```

### 问题3: 文件名大小写问题

**原因**: Windows不区分大小写

**解决**:
```bash
# Git配置为区分大小写
git config core.ignorecase false

# 然后重命名文件
git mv OldName.py new_name.py
```

---

## 📚 参考资源

- [Git官方文档](https://git-scm.com/doc)
- [GitHub官方文档](https://docs.github.com/)
- [约定式提交](https://www.conventionalcommits.org/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)

---

现在您可以安全地使用Git管理项目了！ 🎉
