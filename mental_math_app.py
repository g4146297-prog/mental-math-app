<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ビジネス暗算道場 | 電力・エネルギー＆連結決算特化</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brandBlue: '#1E40AF',
                        brandSky: '#0284C7',
                        bgSlate: '#F8FAFC',
                        cardBg: '#FFFFFF',
                        textDark: '#0F172A',
                        subText: '#475569',
                        accentAmber: '#D97706',
                        accentGreen: '#16A34A',
                        accentRose: '#E11D48'
                    }
                }
            }
        }
    </script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #F1F5F9;
            color: #0F172A;
        }
        .btn-primary {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
            color: white;
            transition: all 0.2s ease;
        }
        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        .card-shadow {
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05), 0 2px 6px -1px rgba(15, 23, 42, 0.03);
        }
    </style>
</head>
<body class="min-h-screen pb-12">

    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
            <div class="flex items-center gap-2 cursor-pointer" onclick="showPage('home')">
                <span class="text-2xl">💼</span>
                <div>
                    <h1 class="font-bold text-lg text-slate-900 leading-tight">ビジネス暗算道場</h1>
                    <p class="text-xs text-slate-500 font-medium">電力・エネルギー ＆ 連結決算特化</p>
                </div>
            </div>
            <button onclick="showPage('home')" class="text-xs font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg transition">
                ホームへ
            </button>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 pt-6">

        <div id="page-home" class="space-y-6">
            <div class="bg-gradient-to-br from-blue-900 to-indigo-900 text-white rounded-2xl p-6 text-center shadow-lg relative overflow-hidden">
                <div class="relative z-10">
                    <span class="inline-block px-3 py-1 bg-blue-500/30 border border-blue-400/30 rounded-full text-xs font-semibold text-blue-200 mb-3">
                        実務直結型・トレーニング (動的問題生成版)
                    </span>
                    <h2 class="text-2xl sm:text-3xl font-extrabold mb-2">桁感とスピードを研ぎ澄ます</h2>
                    <p class="text-xs sm:text-sm text-blue-100/80 max-w-md mx-auto leading-relaxed">
                        電力・エネルギービジネス、海外IPP、連結決算の現場で求められる概算力・ファクトチェック力を鍛えます。
                    </p>
                    <button onclick="showRanking()" class="mt-4 inline-flex items-center gap-1.5 px-4 py-2 bg-white/20 hover:bg-white/30 rounded-full text-sm font-bold text-white transition border border-white/30 backdrop-blur-sm">
                        🏆 スコアランキングを見る
                    </button>
                </div>
            </div>

            <!-- モード選択グリッド -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- 1. お気軽モード -->
                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow flex flex-col justify-between">
                    <div>
                        <div class="flex items-center gap-2 mb-2">
                            <span class="p-2 bg-blue-50 text-blue-600 rounded-lg text-lg">🧩</span>
                            <h3 class="font-bold text-base text-slate-900">お気軽モード（4択式）</h3>
                        </div>
                        <p class="text-xs text-slate-600 mb-4 leading-relaxed">
                            4択から瞬時に正しい金額を選択。スピーディに桁感覚と概算感覚を養います。
                        </p>
                    </div>
                    <div class="space-y-2">
                        <button onclick="startQuiz(false)" class="w-full py-2.5 px-4 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-xl font-bold text-xs transition border border-blue-200 text-left flex justify-between items-center">
                            <span>基礎編（丸い数字・単位付き）</span>
                            <span>→</span>
                        </button>
                        <button onclick="startQuiz(true)" class="w-full py-2.5 px-4 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-bold text-xs transition text-left flex justify-between items-center">
                            <span>上級編（精密数値・規模感ダミー）</span>
                            <span>→</span>
                        </button>
                    </div>
                </div>

                <!-- 2. チャレンジモード -->
                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow flex flex-col justify-between">
                    <div>
                        <div class="flex items-center gap-2 mb-2">
                            <span class="p-2 bg-amber-50 text-amber-600 rounded-lg text-lg">📊</span>
                            <h3 class="font-bold text-base text-slate-900">チャレンジモード（入力式）</h3>
                        </div>
                        <p class="text-xs text-slate-600 mb-4 leading-relaxed">
                            概算値を直接テンキー入力。正解との誤差率（2%以内で満点）でスコアを判定します。
                        </p>
                    </div>
                    <div class="space-y-2">
                        <button onclick="startTraining(false)" class="w-full py-2.5 px-4 bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-xl font-bold text-xs transition border border-amber-200 text-left flex justify-between items-center">
                            <span>基礎編（万・億メイン）</span>
                            <span>→</span>
                        </button>
                        <button onclick="startTraining(true)" class="w-full py-2.5 px-4 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl font-bold text-xs transition text-left flex justify-between items-center">
                            <span>上級編（実戦的桁数）</span>
                            <span>→</span>
                        </button>
                    </div>
                </div>

                <!-- 3. 監査＆ファクトチェック -->
                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow flex flex-col justify-between">
                    <div>
                        <div class="flex items-center gap-2 mb-2">
                            <span class="p-2 bg-rose-50 text-rose-600 rounded-lg text-lg">🔍</span>
                            <h3 class="font-bold text-base text-slate-900">監査＆ファクトチェック</h3>
                        </div>
                        <p class="text-xs text-slate-600 mb-4 leading-relaxed">
                            事業計画やP&Lの抜粋を見て「桁ミス」や「ロジック破綻」を1秒で見破る違和感特訓。
                        </p>
                    </div>
                    <button onclick="AuditModule.start()" class="w-full py-2.5 px-4 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-xl font-bold text-xs transition border border-rose-200 text-left flex justify-between items-center">
                        <span>ミスを見抜く（5問）</span>
                        <span>→</span>
                    </button>
                </div>

                <!-- 4. 感応度特訓 -->
                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow flex flex-col justify-between">
                    <div>
                        <div class="flex items-center gap-2 mb-2">
                            <span class="p-2 bg-emerald-50 text-emerald-600 rounded-lg text-lg">📈</span>
                            <h3 class="font-bold text-base text-slate-900">感応度（センシティビティ）特訓</h3>
                        </div>
                        <p class="text-xs text-slate-600 mb-4 leading-relaxed">
                            為替やJEPX価格の変動による「差分影響額（デルタ）のみ」を素早く弾き出します。
                        </p>
                    </div>
                    <button onclick="SensitivityModule.start()" class="w-full py-2.5 px-4 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-xl font-bold text-xs transition border border-emerald-200 text-left flex justify-between items-center">
                        <span>デルタ暗算（5問）</span>
                        <span>→</span>
                    </button>
                </div>

                <!-- 5. P&L積算シミュレーター -->
                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow flex flex-col justify-between md:col-span-2">
                    <div>
                        <div class="flex items-center gap-2 mb-2">
                            <span class="p-2 bg-purple-50 text-purple-600 rounded-lg text-lg">🏗️</span>
                            <h3 class="font-bold text-base text-slate-900">P&L積算シミュレーター</h3>
                        </div>
                        <p class="text-xs text-slate-600 mb-4 leading-relaxed">
                            CAPEXから最終利益まで、事業投資の構造を連続で構築するトレーニング。毎回異なる数値でプロジェクトを生成します。
                        </p>
                    </div>
                    <button onclick="startPLBuilder()" class="w-full py-2.5 px-4 bg-purple-50 hover:bg-purple-100 text-purple-700 rounded-xl font-bold text-xs transition border border-purple-200 text-left flex justify-between items-center">
                        <span>シミュレーション開始（5ステップ）</span>
                        <span>→</span>
                    </button>
                </div>
            </div>

            <!-- サブコンテンツ -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                <button onclick="startFlashcard()" class="p-4 bg-cyan-50 hover:bg-cyan-100 border border-cyan-200 rounded-2xl text-left transition card-shadow">
                    <span class="text-xl block mb-1">⚡</span>
                    <h4 class="font-bold text-xs text-cyan-900 mb-0.5">フラッシュカード</h4>
                    <p class="text-[11px] text-cyan-700">巨大な桁感覚を瞬時に見抜く</p>
                </button>
                <button onclick="showPage('tips')" class="p-4 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 rounded-2xl text-left transition card-shadow">
                    <span class="text-xl block mb-1">💡</span>
                    <h4 class="font-bold text-xs text-indigo-900 mb-0.5">暗算のコツ (Tips)</h4>
                    <p class="text-[11px] text-indigo-700">プロの実践的ショートカット8選</p>
                </button>
            </div>
        </div>

        <div id="page-ranking" class="hidden space-y-4">
            <div class="flex items-center justify-between">
                <h3 class="font-bold text-slate-900 text-lg flex items-center gap-2">
                    <span>🏆</span> 歴代トップスコア
                </h3>
                <button onclick="showPage('home')" class="text-xs font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg transition">戻る</button>
            </div>

            <div class="bg-white rounded-2xl border border-slate-200 card-shadow overflow-hidden">
                <table class="w-full text-sm text-left">
                    <thead class="bg-slate-50 text-slate-500 text-xs uppercase font-bold">
                        <tr>
                            <th class="px-4 py-3 text-center">順位</th>
                            <th class="px-4 py-3">モード</th>
                            <th class="px-4 py-3 text-right">スコア</th>
                            <th class="px-4 py-3 text-right hidden sm:table-cell">達成日時</th>
                        </tr>
                    </thead>
                    <tbody id="rankingTableBody" class="divide-y divide-slate-100 text-slate-800">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </div>

        <div id="page-game" class="hidden space-y-4">
            <div class="flex items-center justify-between bg-white p-4 rounded-xl border border-slate-200 card-shadow">
                <div>
                    <span id="gameModeTitle" class="text-xs font-bold text-blue-600 uppercase tracking-wide block">MODE</span>
                    <span id="gameProgressText" class="text-sm font-bold text-slate-800">Q.1 / 10</span>
                </div>
                <div class="text-right">
                    <span class="text-xs text-slate-500 font-bold block">SCORE</span>
                    <span id="gameScoreText" class="text-lg font-mono font-bold text-amber-600">0 pts</span>
                </div>
            </div>

            <div class="bg-white p-6 rounded-2xl border border-slate-200 card-shadow space-y-4">
                <span class="text-xs font-bold text-slate-500 uppercase tracking-wider block">QUESTION</span>
                <div id="questionContent" class="text-base sm:text-lg font-bold text-slate-900 leading-relaxed">
                    <!-- Dynamic Question Text -->
                </div>
            </div>

            <div id="timerDisplayContainer" class="font-mono text-amber-600 font-bold text-sm px-2">
                ⏱️ Time: <span id="time_display">0.0</span>s
            </div>

            <div id="trainingInputSection" class="space-y-3 bg-white p-4 rounded-2xl border border-slate-200 card-shadow">
                <label class="block text-xs text-slate-600 font-bold">
                    概算解答を入力 (<span id="inputUnitLabel">円</span>)
                </label>
                <input type="number" id="trainAnswerInput" min="0" step="1" oninput="updateInputPreview()" placeholder="0" class="w-full px-4 py-3 bg-slate-50 border border-slate-300 rounded-xl text-xl text-slate-900 font-mono font-bold focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100">
                
                <div class="grid grid-cols-4 gap-2">
                    <button type="button" onclick="applyQuickKey('trainAnswerInput', '000')" class="py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-mono font-bold text-xs rounded-lg border border-slate-300 transition">
                        +000
                    </button>
                    <button type="button" onclick="applyQuickKey('trainAnswerInput', '万')" class="py-2.5 bg-blue-50 hover:bg-blue-100 text-blue-700 font-bold text-xs rounded-lg border border-blue-200 transition">
                        +万 (×1万)
                    </button>
                    <button type="button" onclick="applyQuickKey('trainAnswerInput', '億')" class="py-2.5 bg-amber-50 hover:bg-amber-100 text-amber-700 font-bold text-xs rounded-lg border border-amber-200 transition">
                        +億 (×1億)
                    </button>
                    <button type="button" onclick="applyQuickKey('trainAnswerInput', 'clear')" class="py-2.5 bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs rounded-lg border border-rose-200 transition">
                        クリア
                    </button>
                </div>

                <div id="inputPreviewText" class="text-xs font-bold text-blue-700 h-5"></div>

                <button id="submitTrainBtn" onclick="submitTrainAnswer()" class="w-full py-3.5 rounded-xl font-bold text-sm btn-primary shadow-md">
                    答え合わせ
                </button>
            </div>

            <div id="quizOptionsSection" class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <!-- Option buttons populated by JS -->
            </div>

            <div id="answerFeedbackPanel" class="hidden space-y-3 bg-white p-5 rounded-2xl border border-slate-200 card-shadow">
                <div id="userAnswerText" class="text-xs text-slate-700 font-medium"></div>
                <div id="correctAnswerText" class="text-base text-slate-900 font-bold"></div>

                <div id="scoreBanner" class="p-3 rounded-xl text-xs font-bold text-center mt-2"></div>

                <button onclick="nextQuestion()" class="w-full py-3 rounded-xl font-bold text-sm btn-primary shadow-md mt-4">
                    次の問題へ
                </button>
            </div>
        </div>

        <div id="page-flashcard" class="hidden space-y-4">
            <div class="flex items-center justify-between">
                <h3 class="font-bold text-slate-900 text-base">⚡ フラッシュカード（巨大桁感特訓）</h3>
                <button onclick="showPage('home')" class="text-xs font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg transition">戻る</button>
            </div>
            <p class="text-xs text-slate-500">最大10兆クラス。ゼロの数を数えずに「万×万＝億」の法則で瞬時に単位を導き出す特訓です。</p>

            <div class="bg-white p-8 rounded-2xl border border-slate-200 card-shadow text-center space-y-6">
                <div id="flashQText" class="text-3xl sm:text-4xl font-mono font-bold text-slate-900 py-4">
                    100万 × 1万
                </div>
                <div id="flashAText" class="hidden text-4xl font-bold text-amber-600 border-t border-dashed border-slate-200 pt-6">
                    100億
                </div>
            </div>

            <div class="flex gap-3">
                <button id="flashShowBtn" onclick="showFlashAnswer()" class="w-full py-3.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold text-sm shadow-md transition">
                    答えを見る
                </button>
                <button id="flashNextBtn" onclick="nextFlashcard()" class="hidden w-full py-3.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl font-bold text-sm shadow-md transition">
                    次のカードへ
                </button>
            </div>
        </div>

        <div id="page-audit" class="hidden space-y-4">
            <div class="flex items-center justify-between">
                <h3 class="font-bold text-slate-900 text-base">🔍 監査＆ファクトチェック</h3>
                <span id="auditProgress" class="text-xs font-bold text-rose-600">Q.1 / 5</span>
            </div>

            <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow space-y-3">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider block">提出された計画・P&L抜粋</span>
                <p id="auditScenarioText" class="text-sm font-bold text-slate-800 leading-relaxed">
                    <!-- Populated by JS -->
                </p>
            </div>

            <div id="auditChoicesSection" class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                <button onclick="AuditModule.check('OK')" class="p-3 bg-white hover:bg-slate-50 border border-slate-200 rounded-xl font-bold text-xs text-slate-800 card-shadow transition">
                    ✅ 正常（問題なし）
                </button>
                <button onclick="AuditModule.check('DIGIT_ERROR')" class="p-3 bg-white hover:bg-amber-50 border border-slate-200 rounded-xl font-bold text-xs text-amber-800 card-shadow transition">
                    ⚠️ 桁ミス（10倍/10分1等）
                </button>
                <button onclick="AuditModule.check('LOGIC_ERROR')" class="p-3 bg-white hover:bg-rose-50 border border-slate-200 rounded-xl font-bold text-xs text-rose-800 card-shadow transition">
                    ❌ 計算ロジック破綻
                </button>
            </div>

            <div id="auditFeedbackPanel" class="hidden space-y-3 bg-white p-4 rounded-2xl border border-slate-200 card-shadow">
                <div id="auditResultText" class="text-xs font-bold"></div>
                <div id="auditExplanationText" class="text-xs text-slate-600 leading-relaxed"></div>
                <button onclick="AuditModule.next()" class="w-full py-3 bg-slate-900 text-white rounded-xl font-bold text-xs shadow-md">
                    次へ
                </button>
            </div>
        </div>

        <div id="page-sensitivity" class="hidden space-y-4">
            <div class="flex items-center justify-between">
                <h3 class="font-bold text-slate-900 text-base">📈 感応度（センシティビティ）特訓</h3>
                <span id="sensProgress" class="text-xs font-bold text-emerald-600">Q.1 / 5</span>
            </div>

            <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow space-y-3">
                <div id="sensBaseText" class="text-xs text-slate-500 bg-slate-50 p-2.5 rounded-lg border border-slate-200"></div>
                <div id="sensQuestionText" class="text-sm font-bold text-slate-900"></div>
            </div>

            <div id="sensInputSection" class="space-y-3 bg-white p-4 rounded-2xl border border-slate-200 card-shadow">
                <label class="block text-xs text-slate-600 font-bold">
                    影響額（絶対値）を入力 (<span id="sensUnitLabel">億円</span>)
                </label>
                <input type="number" id="sensInput" step="0.1" placeholder="0" class="w-full px-4 py-3 bg-slate-50 border border-slate-300 rounded-xl text-xl text-slate-900 font-mono font-bold focus:outline-none focus:border-emerald-600">
                
                <button onclick="SensitivityModule.submit()" class="w-full py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-sm shadow-md transition">
                    判定
                </button>
            </div>

            <div id="sensFeedbackPanel" class="hidden space-y-3 bg-white p-4 rounded-2xl border border-slate-200 card-shadow">
                <div id="sensResultText" class="text-xs font-bold"></div>
                <div id="sensExplanationText" class="text-xs text-slate-600 leading-relaxed"></div>
                <button onclick="SensitivityModule.next()" class="w-full py-3 bg-slate-900 text-white rounded-xl font-bold text-xs shadow-md">
                    次へ
                </button>
            </div>
        </div>

        <div id="page-plbuilder" class="hidden space-y-4">
            <div class="flex items-center justify-between">
                <h3 class="font-bold text-slate-900 text-base">🏗️ P&L積算シミュレーター</h3>
                <span id="plStepProgress" class="text-xs font-bold text-purple-600">Step 1 / 5</span>
            </div>

            <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow space-y-2">
                <span class="text-xs font-bold text-purple-600 uppercase tracking-wider block" id="plProjectTitle">プロジェクト</span>
                <p id="plStepInstruction" class="text-sm font-bold text-slate-900 leading-relaxed"></p>
            </div>

            <div id="plInputArea" class="space-y-3 bg-white p-4 rounded-2xl border border-slate-200 card-shadow">
                <label class="block text-xs text-slate-600 font-bold">
                    算出額を入力 (<span id="plInputUnitLabel">指定の単位</span>)
                </label>
                <input type="number" id="plStepInput" min="0" step="0.01" placeholder="0" class="w-full px-4 py-3 bg-slate-50 border border-slate-300 rounded-xl text-xl text-slate-900 font-mono font-bold focus:outline-none focus:border-purple-600">
                
                <div class="grid grid-cols-3 gap-2">
                    <button type="button" onclick="applyQuickKey('plStepInput', '0.5')" class="py-2 bg-purple-50 hover:bg-purple-100 text-purple-700 font-bold text-xs rounded-lg border border-purple-200 transition">
                        +0.5
                    </button>
                    <button type="button" onclick="applyQuickKey('plStepInput', '1.0')" class="py-2 bg-purple-50 hover:bg-purple-100 text-purple-700 font-bold text-xs rounded-lg border border-purple-200 transition">
                        +1.0
                    </button>
                    <button type="button" onclick="applyQuickKey('plStepInput', 'clear')" class="py-2 bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs rounded-lg border border-rose-200 transition">
                        クリア
                    </button>
                </div>

                <button onclick="PLBuilderModule.submitStep()" class="w-full py-3.5 rounded-xl font-bold text-sm bg-purple-600 hover:bg-purple-700 text-white shadow-md transition">
                    ステップ正解確認
                </button>
            </div>

            <div id="plFeedbackPanel" class="hidden space-y-3 bg-white p-4 rounded-2xl border border-slate-200 card-shadow">
                <div id="plStepResultText" class="text-xs font-bold"></div>
                <div id="plStepExplanation" class="text-xs text-slate-600"></div>
                <button onclick="PLBuilderModule.nextStep()" class="w-full py-3 bg-slate-900 text-white rounded-xl font-bold text-xs shadow-md">
                    次のステップへ
                </button>
            </div>
        </div>

        <div id="page-wrapup" class="hidden space-y-4">
            <div class="bg-white p-6 rounded-2xl border border-slate-200 card-shadow text-center space-y-4">
                <span class="text-3xl">🎉</span>
                <h3 id="wrapupTitle" class="text-xl font-bold text-slate-900">セッション完了</h3>
                
                <div class="py-4 border-y border-slate-100 space-y-2">
                    <div class="text-xs text-slate-500 font-bold uppercase tracking-wider">RESULT SCORE</div>
                    <div id="wrapupScore" class="text-4xl font-mono font-extrabold text-blue-600">5 / 5</div>
                    <div id="wrapupDetail" class="text-xs text-slate-600 font-medium"></div>
                </div>

                <div class="flex gap-3">
                    <button onclick="showPage('home')" class="w-full py-3.5 bg-slate-100 text-slate-700 hover:bg-slate-200 rounded-xl font-bold text-sm transition">
                        トップへ
                    </button>
                    <button onclick="showRanking()" class="w-full py-3.5 btn-primary rounded-xl font-bold text-sm shadow-md">
                        ランキングを見る
                    </button>
                </div>
            </div>
        </div>

        <div id="page-tips" class="hidden space-y-5">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="font-bold text-slate-900 text-lg">💡 プロの実践的・暗算ショートカット8選</h3>
                    <p class="text-xs text-slate-500 mt-0.5">投資銀行・商社・電力ビジネスの現場で「おぉ！」と膝を打つ定石集</p>
                </div>
                <button onclick="showPage('home')" class="text-xs text-blue-600 font-bold bg-blue-50 px-3 py-1.5 rounded-lg border border-blue-200 hover:bg-blue-100 transition">
                    トップへ戻る
                </button>
            </div>

            <div class="space-y-4">
                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1.5 h-full bg-blue-600"></div>
                    <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                        <span class="text-lg">🧮</span> 鉄則1：ゼロを数えるな。「単位の掛け算」を暗記せよ
                    </h4>
                    <p class="text-xs text-slate-700 leading-relaxed mb-3">
                        大きな数字を計算する時、0を数えると必ず桁ミスをします。プロは**「数字部分の計算」と「単位の計算」を完全に分離**して最後にガッチャンコします。
                    </p>
                    <div class="bg-blue-50/60 p-3.5 rounded-xl border border-blue-100 text-xs font-mono text-blue-950 space-y-1.5">
                        <p>・ <b>万 × 万 ＝ 億</b> （10^4 × 10^4 = 10^8）</p>
                        <p>・ <b>億 × 万 ＝ 兆</b> （10^8 × 10^4 = 10^12）</p>
                        <p class="text-[11px] text-blue-800 mt-2 pt-2 border-t border-blue-200/60">
                            【実例】 300万 × 50万<br>
                            ① 数字: 300 × 50 = 15,000<br>
                            ② 単位: 万 × 万 = 億<br>
                            👉 15,000 ＋ 億 ＝ <b>1.5兆円</b>
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1.5 h-full bg-amber-500"></div>
                    <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                        <span class="text-lg">☀️</span> 鉄則2：再エネ特有の「1kW ＝ 約1,000kWh」マジック
                    </h4>
                    <p class="text-xs text-slate-700 leading-relaxed mb-3">
                        太陽光発電の事業計画で、発電量をイチイチ「8760時間×設備利用率(11~13%)」で計算するのは非効率です。掛け合わせると**「約1,000」**になる法則を使います。
                    </p>
                    <div class="bg-amber-50/60 p-3.5 rounded-xl border border-amber-100 text-xs font-mono text-amber-950 space-y-1.5">
                        <p>・ <b>1kWの太陽光 ＝ 年間 約1,000kWh 発電する</b></p>
                        <p class="text-[11px] text-amber-800 mt-2 pt-2 border-t border-amber-200/60">
                            【実例】 出力 50MW（＝5万kW）の太陽光の年間発電量は？<br>
                            👉 「5万 × 1,000」で、瞬時に <b>5,000万kWh</b> とアタリがつきます。
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1.5 h-full bg-emerald-500"></div>
                    <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                        <span class="text-lg">🌐</span> 鉄則3：為替レートの「逆数アプローチ」
                    </h4>
                    <p class="text-xs text-slate-700 leading-relaxed mb-3">
                        「1ドル=150円」の時、日本円をドルにするには「÷150」ですが、桁の大きな割り算は脳に負担がかかります。**「1÷レート」の逆数（掛け算係数）を暗記**しておくのが外資系金融の定石です。
                    </p>
                    <div class="bg-emerald-50/60 p-3.5 rounded-xl border border-emerald-100 text-xs font-mono text-emerald-950 space-y-1.5">
                        <p>・ レート150円の時 ➔ <b>「× 0.66」</b> して桁調整 (1/150 ≒ 0.0066)</p>
                        <p>・ レート125円の時 ➔ <b>「× 0.80」</b> して桁調整 (1/125 ＝ 0.0080)</p>
                        <p class="text-[11px] text-emerald-800 mt-2 pt-2 border-t border-emerald-200/60">
                            【実例】 レート150円で、300億円は何ドル？<br>
                            👉 「300 × 0.66 ＝ 約200」 ➔ 桁を整えて <b>2億ドル</b>。
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1.5 h-full bg-purple-500"></div>
                    <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                        <span class="text-lg">🍕</span> 鉄則4：パーセントは「分数」に変換して割る
                    </h4>
                    <p class="text-xs text-slate-700 leading-relaxed mb-3">
                        「12.5%」や「16.6%」などの中途半端な利益率を掛け算してはいけません。実務によく出る%は、**分母がキリの良い分数に変換**して割り算で処理します。
                    </p>
                    <div class="bg-purple-50/60 p-3.5 rounded-xl border border-purple-100 text-xs font-mono text-purple-950 space-y-1.5">
                        <p>・ <b>12.5%</b> ➔ 「÷ 8」 (1/8)</p>
                        <p>・ <b>16.6%</b> ➔ 「÷ 6」 (1/6)</p>
                        <p>・ <b>37.5%</b> ➔ 「÷ 8 して 3倍」 (3/8)</p>
                        <p class="text-[11px] text-purple-800 mt-2 pt-2 border-t border-purple-200/60">
                            【実例】 売上80億円で、営業利益率12.5%の時の利益額は？<br>
                            👉 80 × 0.125 を真面目にやらず、「80 ÷ 8」で瞬時に <b>10億円</b> と出します。
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1.5 h-full bg-rose-500"></div>
                    <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                        <span class="text-lg">📈</span> 鉄則5：複利と成長率の「72の法則」
                    </h4>
                    <p class="text-xs text-slate-700 leading-relaxed mb-3">
                        投資の価値や事業の売上が**「何年で2倍になるか」**を暗算する黄金の公式です。72を「年利（または年成長率%）」で割るだけで算出できます。
                    </p>
                    <div class="bg-rose-50/60 p-3.5 rounded-xl border border-rose-100 text-xs font-mono text-rose-950 space-y-1.5">
                        <p>・ <b>72 ÷ 年成長率(%) ＝ 2倍になる年数</b></p>
                        <p class="text-[11px] text-rose-800 mt-2 pt-2 border-t border-rose-200/60">
                            【実例】 年率6%で成長する新電車の顧客基盤、何年で倍増する？<br>
                            👉 「72 ÷ 6」で、瞬時に <b>12年</b> と分かります。
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1.5 h-full bg-cyan-500"></div>
                    <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                        <span class="text-lg">⚡</span> 鉄則6：JEPX単価「1円/kWh ＝ 1億kWhで1億円」の黄金比
                    </h4>
                    <p class="text-xs text-slate-700 leading-relaxed mb-3">
                        電力小売や発電事業の感応度分析で最も使われる単位変換の定石です。単位の「1円/kWh」と「1億kWh」が掛け合わさると、そのまま**「1億円」**になります。
                    </p>
                    <div class="bg-cyan-50/60 p-3.5 rounded-xl border border-cyan-100 text-xs font-mono text-cyan-950 space-y-1.5">
                        <p>・ <b>1円/kWh × 1億kWh ＝ 1億円</b></p>
                        <p>・ <b>1円/kWh × 1,000万kWh ＝ 1,000万円</b></p>
                        <p class="text-[11px] text-cyan-800 mt-2 pt-2 border-t border-cyan-200/60">
                            【実例】 契約電力量 3,000万kWh で、調達価格が +2.5円/kWh 上昇した場合の年間インパクトは？<br>
                            👉 「3,000万 × 2.5」 ＝ <b>+7,500万円のコスト増</b> と即答できます。
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1.5 h-full bg-indigo-500"></div>
                    <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                        <span class="text-lg">🏢</span> 鉄則7：連結会計・実効税率「× 0.7」の税後アタリ付け
                    </h4>
                    <p class="text-xs text-slate-700 leading-relaxed mb-3">
                        事業計画や子会社の営業利益から最終純利益（税後）を計算する際、日本の実効税率（約30%）を反映するには**「× 0.7（または ÷ 1.43）」**を適用します。
                    </p>
                    <div class="bg-indigo-50/60 p-3.5 rounded-xl border border-indigo-100 text-xs font-mono text-indigo-950 space-y-1.5">
                        <p>・ <b>税後純利益 ≒ 営業利益 × 0.7</b></p>
                        <p class="text-[11px] text-indigo-800 mt-2 pt-2 border-t border-indigo-200/60">
                            【実例】 新規火力発電事業の税前利益が 120億円。税後インパクトは？<br>
                            👉 「120 × 0.7」 ➔ 「120 × 7 ＝ 840」 で <b>約84億円</b> と導きます。
                        </p>
                    </div>
                </div>

                <div class="bg-white p-5 rounded-2xl border border-slate-200 card-shadow relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1.5 h-full bg-teal-500"></div>
                    <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                        <span class="text-lg">🔋</span> 鉄則8：系統用蓄電池の「1日1.5サイクル・年間550倍」定数
                    </h4>
                    <p class="text-xs text-slate-700 leading-relaxed mb-3">
                        最新のエネルギービジネスで話題の「系統用蓄電池（VPP）」。1日の充放電回数を約1.5サイクルと置くと、定格容量の**年間約550倍**の電力量を充放電できます。
                    </p>
                    <div class="bg-teal-50/60 p-3.5 rounded-xl border border-teal-100 text-xs font-mono text-teal-950 space-y-1.5">
                        <p>・ <b>年間充放電量 ≒ 定格容量(MWh) × 550</b></p>
                        <p class="text-[11px] text-teal-800 mt-2 pt-2 border-t border-teal-200/60">
                            【実例】 容量 100MWh の系統用蓄電池の年間放電量の概算アタリは？<br>
                            👉 「100MWh × 550」 ＝ <b>年間約 55,000MWh (5,500万kWh)</b> と一瞬で判断できます。
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="pt-4 pb-2">
                <button onclick="showPage('home')" class="w-full py-3.5 btn-primary rounded-xl font-bold text-sm shadow-md">
                    トップ画面に戻る
                </button>
            </div>
        </div>

    </main>

    <script>
        // --- 画面切り替え共通関数 ---
        function showPage(pageId) {
            const pages = ['home', 'game', 'flashcard', 'audit', 'sensitivity', 'plbuilder', 'wrapup', 'tips', 'ranking'];
            pages.forEach(p => {
                const el = document.getElementById('page-' + p);
                if (el) el.classList.add('hidden');
            });
            const target = document.getElementById('page-' + pageId);
            if (target) target.classList.remove('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            if(pageId === 'ranking') renderRanking();
        }

        function showRanking() {
            showPage('ranking');
        }

        // --- クイック入力補助 ---
        function applyQuickKey(inputId, type) {
            const input = document.getElementById(inputId);
            if (!input) return;
            let val = parseFloat(input.value) || 0;

            if (type === '000') {
                input.value = val === 0 ? 1000 : Math.round(val * 1000);
            } else if (type === '万') {
                input.value = val === 0 ? 10000 : Math.round(val * 10000);
            } else if (type === '億') {
                input.value = val === 0 ? 100000000 : Math.round(val * 100000000);
            } else if (type === '0.5') {
                input.value = (val + 0.5).toFixed(1);
            } else if (type === '1.0') {
                input.value = (val + 1.0).toFixed(1);
            } else if (type === 'clear') {
                input.value = '';
            }

            if (inputId === 'trainAnswerInput') {
                updateInputPreview();
            }
        }

        function updateInputPreview() {
            const val = parseFloat(document.getElementById('trainAnswerInput').value) || 0;
            const previewEl = document.getElementById('inputPreviewText');
            if (val <= 0) {
                previewEl.innerText = '';
                return;
            }
            previewEl.innerText = 'プレビュー: ' + formatJapanese(val);
        }

        function formatJapanese(num) {
            if (!num || isNaN(num)) return '0';
            const units = [
                { val: 1e12, name: '兆' },
                { val: 1e8, name: '億' },
                { val: 1e4, name: '万' }
            ];
            let res = '';
            let rem = Math.abs(num);
            for (let u of units) {
                if (rem >= u.val) {
                    let v = Math.floor(rem / u.val);
                    rem %= u.val;
                    res += v.toLocaleString() + u.name;
                }
            }
            if (rem > 0 || res === '') {
                res += Math.round(rem).toLocaleString();
            }
            return (num < 0 ? '-' : '') + res;
        }

        function formatNumberWithUnitLabel(v) {
            if (v >= 1e12 && v % 1e12 === 0) return (v / 1e12) + '兆';
            if (v >= 1e8 && v % 1e8 === 0) return (v / 1e8) + '億';
            if (v >= 1e4 && v % 1e4 === 0) return (v / 1e4) + '万';
            return v.toLocaleString();
        }

        // --- 改良版: 対数スケールによる均等「丸い数字」生成ロジック ---
        function getSmartNumber(min, max, isAdvanced) {
            if (isAdvanced) {
                return Math.floor(Math.random() * (max - min + 1)) + min;
            }
            
            // 範囲内の桁数（power）を求める
            let minPower = Math.floor(Math.log10(min));
            let maxPower = Math.floor(Math.log10(max));
            
            // 存在し得る桁数を配列化
            let availablePowers = [];
            for (let p = minPower; p <= maxPower; p++) {
                availablePowers.push(p);
            }
            
            // 桁数を均等な確率で選定
            let chosenPower = availablePowers[Math.floor(Math.random() * availablePowers.length)];
            
            // 豊富な暗算向き倍率候補（偏りをなくす）
            let bases = [1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8];
            let candidates = [];
            for (let b of bases) {
                let val = Math.round(b * Math.pow(10, chosenPower));
                if (val >= min && val <= max) {
                    candidates.push(val);
                }
            }
            
            if (candidates.length > 0) {
                return candidates[Math.floor(Math.random() * candidates.length)];
            }
            
            // フォールバック
            return Math.floor(Math.random() * (max - min + 1)) + min;
        }

        function getSmartPct(min, max, isAdvanced) {
            if (isAdvanced) {
                return Math.floor(Math.random() * (max - min + 1)) + min;
            }
            const cleanPcts = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 75, 80].filter(p => p >= min && p <= max);
            return cleanPcts.length ? cleanPcts[Math.floor(Math.random() * cleanPcts.length)] : min;
        }

        function getSmartRate(min, max, isAdvanced) {
            if (isAdvanced) {
                return Math.floor(Math.random() * (max - min + 1)) + min;
            }
            const raw = Math.floor(Math.random() * (max - min + 1)) + min;
            if (max <= 10) return raw; // タイバーツなど小範囲はそのまま
            return Math.round(raw / 5) * 5; 
        }

        // --- プロシージャル動的問題生成エンジン ---
        const PROC_GEN_DB = {
            regions: ["北米", "欧州", "豪州", "東南アジア", "国内", "中東"],
            assets: [
                { name: "洋上風力発電", unit1: "kW", range1: [10000, 500000], unit2: "円/kW", range2: [120000, 250000] },
                { name: "メガソーラー", unit1: "kW", range1: [5000, 200000], unit2: "円/kW", range2: [80000, 140000] },
                { name: "系統用蓄電池", unit1: "kWh", range1: [10000, 200000], unit2: "円/kWh", range2: [40000, 80000] },
                { name: "コーポレートPPA", unit1: "kWh", range1: [100000, 100000000], unit2: "円/kWh", range2: [12, 25] },
                { name: "バイオマス発電", unit1: "kWh", range1: [1000000, 50000000], unit2: "円/kWh", range2: [18, 32] },
                { name: "水素プラント", unit1: "kg", range1: [100000, 5000000], unit2: "円/kg", range2: [500, 1200] }
            ],
            fx: [
                { currency: "ドル", rateRange: [140, 160] },
                { currency: "ユーロ", rateRange: [150, 170] },
                { currency: "ポンド", rateRange: [180, 200] },
                { currency: "豪ドル", rateRange: [90, 110] },
                { currency: "バーツ", rateRange: [4, 5] }
            ]
        };

        let gameState = {
            mode: 'quiz',
            isAdvanced: false,
            currentQ: 1,
            totalQ: 10,
            score: 0,
            startTime: 0,
            timerInterval: null,
            currentQData: null
        };

        function startQuiz(advanced) {
            gameState.mode = 'quiz';
            gameState.isAdvanced = advanced;
            initGameSession();
        }

        function startTraining(advanced) {
            gameState.mode = 'training';
            gameState.isAdvanced = advanced;
            initGameSession();
        }

        function initGameSession() {
            gameState.currentQ = 1;
            gameState.score = 0;
            document.getElementById('gameModeTitle').innerText = (gameState.mode === 'quiz' ? 'お気軽4択' : 'チャレンジ入力') + (gameState.isAdvanced ? ' (上級)' : ' (基礎)');
            showPage('game');
            loadQuestion();
        }

        function generateProceduralQuestion(isAdv) {
            const pat = Math.floor(Math.random() * 3); // 0: 単純掛け算, 1: 割合%, 2: 為替換算
            const region = PROC_GEN_DB.regions[Math.floor(Math.random() * PROC_GEN_DB.regions.length)];
            const asset = PROC_GEN_DB.assets[Math.floor(Math.random() * PROC_GEN_DB.assets.length)];
            const fxItem = PROC_GEN_DB.fx[Math.floor(Math.random() * PROC_GEN_DB.fx.length)];

            if (pat === 0) { // 単純掛け算 (数量 × 単価)
                const val1 = getSmartNumber(asset.range1[0], asset.range1[1], isAdv);
                const val2 = getSmartNumber(asset.range2[0], asset.range2[1], isAdv);
                const correct = val1 * val2;
                const label1Str = isAdv ? val1.toLocaleString() : formatNumberWithUnitLabel(val1);
                const label2Str = isAdv ? val2.toLocaleString() : formatNumberWithUnitLabel(val2);
                
                const qText = `${region}での<b>${asset.name}</b>事業（規模 <b>${label1Str}${asset.unit1}</b>）。単価 <b>${label2Str}${asset.unit2}</b> のとき、総額は？`;
                return { qText, correct, pattern: 1, raw_val1: val1, raw_val2: val2 };

            } else if (pat === 1) { // 割合 (売上/簿価 × %)
                const val1 = getSmartNumber(100000000, 100000000000, isAdv);
                const pct = getSmartPct(10, 50, isAdv);
                const correct = val1 * (pct / 100);
                const label1Str = isAdv ? val1.toLocaleString() : formatNumberWithUnitLabel(val1);

                const topics = [
                    `${region}の<b>${asset.name}</b>プロジェクト（年間売上 <b>${label1Str}円</b>）。営業利益率 <b>${pct}%</b> のとき利益額は？`,
                    `${region}事業（総利益 <b>${label1Str}円</b>）。自社の持分比率 <b>${pct}%</b> のとき持分法投資損益は？`,
                    `出資会社でのれん残高 <b>${label1Str}円</b>。評価見直しで <b>${pct}%</b> の減損損失を計上。減損額は？`
                ];
                const qText = topics[Math.floor(Math.random() * topics.length)];
                return { qText, correct, pattern: 2, raw_val1: val1, raw_pct: pct };

            } else { // 為替換算 (広範囲の外貨額 × レート)
                const val1 = getSmartNumber(100000, 500000000, isAdv); // 10万〜5億外貨
                const rate = getSmartRate(fxItem.rateRange[0], fxItem.rateRange[1], isAdv);
                const correct = val1 * rate;
                const label1Str = isAdv ? val1.toLocaleString() : formatNumberWithUnitLabel(val1);

                const qText = `${region}の<b>${asset.name}</b>事業で得た現地利益 <b>${label1Str}${fxItem.currency}</b>。為替レート 1${fxItem.currency}=<b>${rate}円</b> のとき円換算額は？`;
                return { qText, correct, pattern: 5, raw_val1: val1, raw_val2: rate, currency: fxItem.currency };
            }
        }

        function loadQuestion() {
            document.getElementById('gameProgressText').innerText = `Q.${gameState.currentQ} / ${gameState.totalQ}`;
            document.getElementById('gameScoreText').innerText = `${gameState.score} pts`;
            document.getElementById('answerFeedbackPanel').classList.add('hidden');
            document.getElementById('trainAnswerInput').value = '';
            document.getElementById('inputPreviewText').innerText = '';

            const qData = generateProceduralQuestion(gameState.isAdvanced);
            gameState.currentQData = qData;

            document.getElementById('questionContent').innerHTML = qData.qText;

            if (gameState.mode === 'training') {
                document.getElementById('trainingInputSection').classList.remove('hidden');
                document.getElementById('quizOptionsSection').classList.add('hidden');
            } else {
                document.getElementById('trainingInputSection').classList.add('hidden');
                document.getElementById('quizOptionsSection').classList.remove('hidden');
                renderQuizOptions(qData.correct);
            }

            startTimer();
        }

        // 4択選択肢の安全生成（ユニークな4選択肢を保証）
        function renderQuizOptions(correct) {
            const container = document.getElementById('quizOptionsSection');
            container.innerHTML = '';
            
            let optsSet = new Set([correct]);
            
            if (gameState.isAdvanced) {
                const multipliers = [0.5, 0.7, 1.5, 2.0, 3.0, 0.3, 2.5];
                for (let m of multipliers) {
                    if (optsSet.size >= 4) break;
                    let candidate = Math.round(correct * m);
                    if (candidate > 0 && candidate !== correct) optsSet.add(candidate);
                }
            } else {
                const multipliers = [10, 0.1, 5, 2, 0.5, 100];
                for (let m of multipliers) {
                    if (optsSet.size >= 4) break;
                    let candidate = Math.round(correct * m);
                    if (candidate > 0 && candidate !== correct) optsSet.add(candidate);
                }
            }

            let factor = 1.2;
            while (optsSet.size < 4) {
                let candidate = Math.round(correct * factor);
                if (candidate !== correct) optsSet.add(candidate);
                factor += 0.3;
            }

            let opts = Array.from(optsSet).sort(() => Math.random() - 0.5);

            opts.forEach(opt => {
                const btn = document.createElement('button');
                btn.className = "p-4 bg-white hover:bg-blue-50 border border-slate-200 rounded-xl font-bold text-sm text-slate-800 card-shadow transition text-center";
                btn.innerText = formatJapanese(opt) + ' 円';
                btn.onclick = () => submitQuizOption(opt);
                container.appendChild(btn);
            });
        }

        function startTimer() {
            gameState.startTime = Date.now();
            clearInterval(gameState.timerInterval);
            gameState.timerInterval = setInterval(() => {
                const delta = ((Date.now() - gameState.startTime) / 1000).toFixed(1);
                document.getElementById('time_display').innerText = delta;
            }, 100);
        }

        function stopTimer() {
            clearInterval(gameState.timerInterval);
        }

        function submitTrainAnswer() {
            stopTimer();
            const userVal = parseFloat(document.getElementById('trainAnswerInput').value) || 0;
            const correct = gameState.currentQData.correct;
            const diffPct = Math.abs(userVal - correct) / (correct || 1);
            let pts = 0;
            if (diffPct <= 0.02) pts = 10;
            else if (diffPct <= 0.05) pts = 8;
            else if (diffPct <= 0.1) pts = 5;

            gameState.score += pts;
            showAnswerFeedback(userVal, correct, pts, diffPct);
        }

        function submitQuizOption(selectedOpt) {
            stopTimer();
            const correct = gameState.currentQData.correct;
            const isCorrect = selectedOpt === correct;
            const pts = isCorrect ? 10 : 0;
            gameState.score += pts;
            showAnswerFeedback(selectedOpt, correct, pts, isCorrect ? 0 : 1);
        }

        function showAnswerFeedback(userVal, correct, pts, diffPct) {
            document.getElementById('answerFeedbackPanel').classList.remove('hidden');
            document.getElementById('userAnswerText').innerText = `あなたの回答: ${formatJapanese(userVal)} 円`;
            document.getElementById('correctAnswerText').innerText = `正解: ${formatJapanese(correct)} 円 (${correct.toLocaleString()}円)`;
            
            const banner = document.getElementById('scoreBanner');
            if (pts === 10) {
                banner.innerText = "⭕ 完全正解！ (+10 pts)";
                banner.className = "p-3 rounded-xl text-xs font-bold text-center bg-emerald-50 text-emerald-700 border border-emerald-200";
            } else if (pts > 0) {
                banner.innerText = `⚠️ 概算クリア！（誤差 ${(diffPct*100).toFixed(1)}% / +${pts} pts)`;
                banner.className = "p-3 rounded-xl text-xs font-bold text-center bg-amber-50 text-amber-700 border border-amber-200";
            } else {
                banner.innerText = "❌ 乖離が大きすぎます (+0 pts)";
                banner.className = "p-3 rounded-xl text-xs font-bold text-center bg-rose-50 text-rose-700 border border-rose-200";
            }
        }

        function nextQuestion() {
            if (gameState.currentQ >= gameState.totalQ) {
                saveScore(gameState.mode, gameState.isAdvanced, gameState.score);
                showWrapup("通常セッション完了", `${gameState.score} / ${gameState.totalQ * 10} pts`, "おつかれさまでした！概算暗算の感覚が高まりました。");
            } else {
                gameState.currentQ++;
                loadQuestion();
            }
        }

        function saveScore(mode, isAdvanced, score) {
            try {
                let history = JSON.parse(localStorage.getItem('bizMathScoreHistory')) || [];
                const modeName = (mode === 'quiz' ? 'お気軽4択' : 'チャレンジ') + (isAdvanced ? '(上級)' : '(基礎)');
                const d = new Date();
                history.push({
                    date: d.toLocaleDateString('ja-JP', { month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit' }),
                    mode: modeName,
                    score: score
                });
                history.sort((a, b) => b.score - a.score);
                history = history.slice(0, 10); 
                localStorage.setItem('bizMathScoreHistory', JSON.stringify(history));
            } catch (e) {
                console.warn("Local storage error", e);
            }
        }

        function renderRanking() {
            const tbody = document.getElementById('rankingTableBody');
            tbody.innerHTML = '';
            try {
                let history = JSON.parse(localStorage.getItem('bizMathScoreHistory')) || [];
                if (history.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-slate-500 text-xs">まだスコア履歴がありません</td></tr>';
                    return;
                }
                history.forEach((h, i) => {
                    const tr = document.createElement('tr');
                    tr.className = "border-b border-slate-100";
                    tr.innerHTML = `
                        <td class="py-3 text-center text-slate-500 font-bold">${i + 1}</td>
                        <td class="py-3 font-medium text-slate-700 text-xs">${h.mode}</td>
                        <td class="py-3 text-right font-bold text-blue-600">${h.score} <span class="text-[10px]">pts</span></td>
                        <td class="py-3 text-right text-[10px] text-slate-400 hidden sm:table-cell">${h.date}</td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch(e) {
                tbody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-rose-500 text-xs">履歴の読み込みに失敗しました</td></tr>';
            }
        }

        function showWrapup(title, scoreText, detailText) {
            document.getElementById('wrapupTitle').innerText = title;
            document.getElementById('wrapupScore').innerText = scoreText;
            document.getElementById('wrapupDetail').innerText = detailText;
            showPage('wrapup');
        }

        // フラッシュカード機能
        function startFlashcard() {
            showPage('flashcard');
            nextFlashcard();
        }

        function nextFlashcard() {
            let p1, p2;
            do {
                p1 = Math.floor(Math.random() * 9) + 2; 
                p2 = Math.floor(Math.random() * 9) + 2; 
            } while (p1 + p2 > 13); 

            const v1 = Math.pow(10, p1);
            const v2 = Math.pow(10, p2);
            
            document.getElementById('flashQText').innerText = `${formatNumberWithUnitLabel(v1)} × ${formatNumberWithUnitLabel(v2)}`;
            document.getElementById('flashAText').innerText = formatJapanese(v1 * v2);
            document.getElementById('flashAText').classList.add('hidden');
            document.getElementById('flashShowBtn').classList.remove('hidden');
            document.getElementById('flashNextBtn').classList.add('hidden');
        }

        function showFlashAnswer() {
            document.getElementById('flashAText').classList.remove('hidden');
            document.getElementById('flashShowBtn').classList.add('hidden');
            document.getElementById('flashNextBtn').classList.remove('hidden');
        }

        const AuditModule = {
            currentQ: 1,
            score: 0,
            currentScenario: null,
            generateQuestion() {
                const noiseType = ["OK", "DIGIT_ERROR", "LOGIC_ERROR"][Math.floor(Math.random() * 3)];
                const baseVal1 = getSmartNumber(1000, 50000, false);
                const baseVal2 = getSmartNumber(10, 50, false);
                const trueAns = baseVal1 * baseVal2;

                let text = "";
                let exp = "";

                if (noiseType === "OK") {
                    text = `年間発電量 ${formatNumberWithUnitLabel(baseVal1 * 10000)}kWh × 単価 ${baseVal2}円/kWh ＝ 年間売上 ${formatJapanese(trueAns * 10000)}`;
                    exp = `正常です。（${formatNumberWithUnitLabel(baseVal1 * 10000)} × ${baseVal2}円 ＝ ${formatJapanese(trueAns * 10000)}）`;
                } else if (noiseType === "DIGIT_ERROR") {
                    const digitErrAns = trueAns * 10;
                    text = `年間発電量 ${formatNumberWithUnitLabel(baseVal1 * 10000)}kWh × 単価 ${baseVal2}円/kWh ＝ 年間売上 ${formatJapanese(digitErrAns * 10000)}`;
                    exp = `桁ミスです。正しくは ${formatJapanese(trueAns * 10000)}（${digitErrAns >= trueAns ? "10倍過大" : "10分1過小"}）です。`;
                } else {
                    text = `売上高 ${formatJapanese(baseVal1 * 100000)}円、営業利益 ${formatJapanese(baseVal2 * 100000)}円 のとき、営業利益率は 5% である。`;
                    exp = `計算ロジック破綻です。利益率は (${baseVal2 * 100000} ÷ ${baseVal1 * 100000}) ＝ 約${((baseVal2/baseVal1)*100).toFixed(1)}% です。`;
                }

                return { text, correct: noiseType, exp };
            },
            start() {
                this.currentQ = 1;
                this.score = 0;
                showPage('audit');
                this.load();
            },
            load() {
                document.getElementById('auditProgress').innerText = `Q.${this.currentQ} / 5`;
                document.getElementById('auditFeedbackPanel').classList.add('hidden');
                this.currentScenario = this.generateQuestion();
                document.getElementById('auditScenarioText').innerHTML = this.currentScenario.text;
            },
            check(choice) {
                const isCorrect = choice === this.currentScenario.correct;
                if (isCorrect) this.score++;

                document.getElementById('auditFeedbackPanel').classList.remove('hidden');
                document.getElementById('auditResultText').innerText = isCorrect ? "🎉 正解！違和感を検知しました。" : "❌ 不正解... 見落としがあります。";
                document.getElementById('auditExplanationText').innerText = this.currentScenario.exp;
            },
            next() {
                if (this.currentQ >= 5) {
                    saveScore("監査＆ファクトチェック", false, this.score * 10);
                    showWrapup("監査＆ファクトチェック完了", `${this.score} / 5 正解`, "事業計画や数値の違和感センサーが研ぎ澄まされました。");
                } else {
                    this.currentQ++;
                    this.load();
                }
            }
        };

        const SensitivityModule = {
            currentQ: 1,
            score: 0,
            currentScenario: null,
            generateQuestion() {
                const type = Math.floor(Math.random() * 4);
                let base = "", q = "", correct = 0, exp = "";

                if (type === 0) { // 為替デルタ
                    const fxBase = getSmartNumber(1, 10, false);
                    const rateDelta = Math.floor(Math.random() * 4) + 2;
                    correct = parseFloat((fxBase * rateDelta).toFixed(1));
                    base = `ベースライン: ドル円150円のとき、海外事業利益 ${formatJapanese(fxBase * 100000000 * 150)} (${fxBase}億ドル)`;
                    q = `ドル円が +${rateDelta}円 円安に進んだ場合の影響額（増分デルタ）は？`;
                    exp = `正解: +${correct}億円 (${fxBase}億ドル × ${rateDelta}円 = ${correct}億円)。`;
                } else if (type === 1) { // JEPXデルタ
                    const volume = getSmartNumber(1000, 10000, false);
                    const priceDelta = (Math.floor(Math.random() * 5) + 1) * 0.5;
                    correct = parseFloat(((volume / 10000) * priceDelta).toFixed(2));
                    base = `ベースライン: 年間調達量 ${formatNumberWithUnitLabel(volume * 10000)}kWh の電力事業`;
                    q = `JEPX価格が +${priceDelta}円/kWh 上昇した場合の「調達コスト増加額」は？`;
                    exp = `正解: +${correct}億円 (${formatNumberWithUnitLabel(volume * 10000)}kWh × ${priceDelta}円 = ${correct}億円)。`;
                } else if (type === 2) { // 稼働率デルタ
                    const revBase = getSmartNumber(50, 300, false);
                    const dropPct = Math.floor(Math.random() * 5) + 1;
                    correct = parseFloat((revBase * (dropPct / 100)).toFixed(1));
                    base = `ベースライン: 年間売上高 ${revBase}億円（設備稼働率 100%想定）`;
                    q = `トラブルで年間稼働率が ${dropPct}% 低下した場合の「減収額」は？`;
                    exp = `正解: ${correct}億円 (${revBase}億円 × ${dropPct}% = ${correct}億円)。`;
                } else { // 金利デルタ
                    const debtBase = getSmartNumber(100, 1000, false);
                    const rateUp = (Math.floor(Math.random() * 4) + 1) * 0.25;
                    correct = parseFloat((debtBase * (rateUp / 100)).toFixed(2));
                    base = `ベースライン: プロジェクト借入金 ${debtBase}億円`;
                    q = `ベース金利が +${rateUp}% 上昇した場合の年間の「支払利息増加額」は？`;
                    exp = `正解: ${correct}億円 (${debtBase}億円 × ${rateUp}% = ${correct}億円)。`;
                }

                return { base, q, correct, exp };
            },
            start() {
                this.currentQ = 1;
                this.score = 0;
                showPage('sensitivity');
                this.load();
            },
            load() {
                document.getElementById('sensProgress').innerText = `Q.${this.currentQ} / 5`;
                document.getElementById('sensFeedbackPanel').classList.add('hidden');
                document.getElementById('sensInput').value = '';
                this.currentScenario = this.generateQuestion();
                document.getElementById('sensBaseText').innerText = this.currentScenario.base;
                document.getElementById('sensQuestionText').innerText = this.currentScenario.q;
            },
            submit() {
                const val = parseFloat(document.getElementById('sensInput').value) || 0;
                const isCorrect = Math.abs(val - this.currentScenario.correct) <= 0.05;
                if (isCorrect) this.score++;

                document.getElementById('sensFeedbackPanel').classList.remove('hidden');
                document.getElementById('sensResultText').innerText = isCorrect ? "⭕ 正解！" : "❌ 不正解";
                document.getElementById('sensExplanationText').innerText = this.currentScenario.exp;
            },
            next() {
                if (this.currentQ >= 5) {
                    saveScore("感応度特訓", false, this.score * 10);
                    showWrapup("感応度特訓完了", `${this.score} / 5 正解`, "差分（デルタ）のみを速算するプロのテクニックが身につきました。");
                } else {
                    this.currentQ++;
                    this.load();
                }
            }
        };

        const PLBuilderModule = {
            currentStep: 1,
            score: 0,
            activeProject: null,
            generateProject() {
                const type = Math.floor(Math.random() * 2);
                if (type === 0) { // 太陽光プロジェクト
                    const mw = (Math.floor(Math.random() * 8) + 2) * 10;
                    const unitCapex = (Math.floor(Math.random() * 6) + 15);
                    const capex = (mw * 1000 * unitCapex) / 10000;

                    const genKwh = mw * 1000 * 1200;
                    const genManKwh = genKwh / 10000;
                    const fitPrice = 15;
                    const revenue = (genKwh * fitPrice) / 100000000;

                    const opexPct = 20;
                    const opex = parseFloat((revenue * 0.2).toFixed(1));
                    const dep = capex / 20;
                    const opProfit = parseFloat((revenue - opex - dep).toFixed(1));

                    return {
                        title: `プロジェクト: ${mw}MW 太陽光発電所`,
                        steps: [
                            { q: `Step 1 (投資): 出力 ${mw}MW (${mw*1000}kW) × 建設単価 ${unitCapex}万円/kW の総投資額(CAPEX)は？(億円)`, correct: capex, exp: `${mw*1000}kW × ${unitCapex}万円 ＝ ${capex}億円` },
                            { q: `Step 2 (売上): 年間発電量 ${genManKwh.toLocaleString()}万kWh × 買取単価 ${fitPrice}円/kWh の年間売上は？(億円)`, correct: revenue, exp: `${genManKwh.toLocaleString()}万kWh × ${fitPrice}円 ＝ ${revenue}億円` },
                            { q: `Step 3 (OPEX): 売上 ${revenue}億円 の ${opexPct}% が運営維持費の場合の金額は？(億円)`, correct: opex, exp: `${revenue}億 × ${opexPct}% ＝ ${opex}億円` },
                            { q: `Step 4 (償却): CAPEX ${capex}億円 ÷ 20年（定額法）の年間減価償却費は？(億円)`, correct: dep, exp: `${capex}億 ÷ 20年 ＝ ${dep}億円` },
                            { q: `Step 5 (利益): 売上 ${revenue}億 － OPEX ${opex}億 － 償却費 ${dep}億 ＝ 営業利益は？(億円)`, correct: opProfit, exp: `${revenue} － ${opex} － ${dep} ＝ ${opProfit}億円` }
                        ]
                    };
                } else { // 系統用蓄電池プロジェクト
                    const mwh = (Math.floor(Math.random() * 5) + 5) * 10;
                    const unitPrice = 6;
                    const capex = (mwh * 1000 * unitPrice) / 10000;

                    const cycles = 500;
                    const genManKwh = (mwh * 1000 * cycles) / 10000;
                    const spread = 10;
                    const grossProfit = (genManKwh * 10000 * spread) / 100000000;

                    const opex = parseFloat((capex * 0.02).toFixed(1));
                    const ebitda = parseFloat((grossProfit - opex).toFixed(1));

                    return {
                        title: `プロジェクト: ${mwh}MWh 系統用蓄電池`,
                        steps: [
                            { q: `Step 1 (投資): 容量 ${mwh}MWh (${mwh*1000}kWh) × 単価 ${unitPrice}万円/kWh の総投資額(CAPEX)は？(億円)`, correct: capex, exp: `${mwh*1000}kWh × ${unitPrice}万円 ＝ ${capex}億円` },
                            { q: `Step 2 (取引量): 容量 ${mwh}MWh × 年間${cycles}サイクルの年間充放電量は？(万kWh)`, correct: genManKwh, exp: `${mwh*1000}kWh × ${cycles}回 ＝ ${genManKwh.toLocaleString()}万kWh` },
                            { q: `Step 3 (粗利): 年間 ${genManKwh.toLocaleString()}万kWh × スプレッド ${spread}円/kWh の粗利益は？(億円)`, correct: grossProfit, exp: `${genManKwh.toLocaleString()}万kWh × ${spread}円 ＝ ${grossProfit}億円` },
                            { q: `Step 4 (OPEX): 投資額 ${capex}億円 の 2% が年間維持費(OPEX)の場合の金額は？(億円)`, correct: opex, exp: `${capex}億 × 2% ＝ ${opex}億円` },
                            { q: `Step 5 (利益): 粗利 ${grossProfit}億 － OPEX ${opex}億 ＝ EBITDA(償却前利益)は？(億円)`, correct: ebitda, exp: `${grossProfit} － ${opex} ＝ ${ebitda}億円` }
                        ]
                    };
                }
            },
            startPLBuilder() {
                this.currentStep = 1;
                this.score = 0;
                this.activeProject = this.generateProject();
                showPage('plbuilder');
                this.loadStep();
            },
            loadStep() {
                document.getElementById('plStepProgress').innerText = `Step ${this.currentStep} / 5`;
                document.getElementById('plFeedbackPanel').classList.add('hidden');
                document.getElementById('plStepInput').value = '';

                const s = this.activeProject.steps[this.currentStep - 1];
                document.getElementById('plProjectTitle').innerText = this.activeProject.title;
                document.getElementById('plStepInstruction').innerText = s.q;
            },
            submitStep() {
                const val = parseFloat(document.getElementById('plStepInput').value) || 0;
                const s = this.activeProject.steps[this.currentStep - 1];
                
                const isCorrect = Math.abs(val - s.correct) <= 0.05;
                if (isCorrect) this.score++;

                document.getElementById('plFeedbackPanel').classList.remove('hidden');
                document.getElementById('plStepResultText').innerText = isCorrect ? "⭕ 正解！" : "❌ 不正解...";
                document.getElementById('plStepResultText').className = isCorrect ? "text-xs font-bold text-emerald-600" : "text-xs font-bold text-rose-600";
                document.getElementById('plStepExplanation').innerText = s.exp;
            },
            nextStep() {
                if (this.currentStep >= 5) {
                    saveScore("P&L積算", false, this.score * 10);
                    showWrapup("P&L積算完了", `${this.score} / 5 正解`, "新規事業の投資から損益構造までを脳内に構築できました！");
                } else {
                    this.currentStep++;
                    this.loadStep();
                }
            }
        };

        function startPLBuilder() {
            PLBuilderModule.startPLBuilder();
        }

        // 初期ロード時処理
        window.onload = function() {
            showPage('home');
        };
    </script>
</body>
</html>
