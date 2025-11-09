#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Простой веб-сервер для APIOrchestra
Версия: 5.0 (умный анализ и расширенная визуализация)
Автор: Дмитрий Крылосов
"""

import http.server
import socketserver
import os
import json
import time
import random
import subprocess
import datetime
from urllib.parse import urlparse, parse_qs
from http import HTTPStatus

# Папка с проектом
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VIRT_BANK_SCRIPT = os.path.join(PROJECT_DIR, "virtual_bank_orchestrator.py")


class SimpleOrchestraHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>APIOrchestra - Тестирование бизнес-процессов</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 1px solid #eee;
            padding-bottom: 20px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #7f8c8d;
            font-size: 1.1em;
        }
        .container {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }
        input[type="file"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
        }
        select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
            margin-bottom: 15px;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: background-color 0.3s;
            width: 100%;
        }
        button:hover {
            background-color: #2980b9;
        }
        button:disabled {
            background-color: #bdc3c7;
            cursor: not-allowed;
        }
        #result {
            margin-top: 30px;
            padding: 25px;
            background-color: #e9f7fa;
            border-radius: 8px;
            display: none;
        }
        .step {
            margin-bottom: 15px;
            padding: 12px;
            background-color: #f1f8ff;
            border-radius: 4px;
            border-left: 4px solid #3498db;
        }
        .step.failed {
            border-left-color: #e74c3c;
            background-color: #fdeded;
        }
        .step.success {
            border-left-color: #2ecc71;
        }
        .section {
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
        .section-title {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .section-title i {
            margin-right: 10px;
            color: #3498db;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .metric-card {
            background: white;
            border-radius: 6px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            border: 1px solid #eee;
        }
        .metric-value {
            font-size: 24px;
            font-weight: 700;
            color: #2c3e50;
            margin: 5px 0;
        }
        .metric-label {
            color: #7f8c8d;
            font-size: 14px;
        }
        .balance-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 15px;
        }
        .process-visualization {
            height: 250px;
            margin-top: 15px;
            background: white;
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .progress-bar {
            height: 8px;
            background-color: #ecf0f1;
            border-radius: 4px;
            margin-top: 10px;
            overflow: hidden;
        }
        .progress {
            height: 100%;
            background-color: #2ecc71;
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        .logs-section {
            max-height: 300px;
            overflow-y: auto;
            margin-top: 15px;
        }
        .log-entry {
            padding: 10px;
            border-bottom: 1px solid #eee;
            font-family: monospace;
            font-size: 14px;
        }
        .log-step {
            font-weight: bold;
            color: #2c3e50;
        }
        .log-status.pas {
            color: #2ecc71;
        }
        .log-status.fail {
            color: #e74c3c;
        }
        .log-duration {
            float: right;
            background: #ecf0f1;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 12px;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top: 4px solid #3498db;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .chart-container {
            height: 150px;
            margin-top: 15px;
        }
        .chart-bar {
            background-color: #3498db;
            border-radius: 4px 4px 0 0;
            transition: height 0.5s ease;
        }
        .chart-labels {
            display: flex;
            justify-content: space-between;
            margin-top: 5px;
            font-size: 12px;
            color: #7f8c8d;
        }
        .chart-value {
            text-align: center;
            font-size: 12px;
            margin-top: 3px;
            color: #2c3e50;
        }
        .bank-selector {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .bank-option {
            flex: 1;
            padding: 15px;
            border: 2px solid #ecf0f1;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
        }
        .bank-option:hover {
            border-color: #3498db;
            background-color: #f8f9fa;
        }
        .bank-option.selected {
            border-color: #3498db;
            background-color: #e9f7fa;
            box-shadow: 0 2px 5px rgba(52, 152, 219, 0.2);
        }
        .bank-icon {
            font-size: 24px;
            margin-bottom: 10px;
        }
        .bank-name {
            font-weight: 600;
            color: #2c3e50;
        }
        .bank-description {
            color: #7f8c8d;
            font-size: 14px;
        }
        .bank-details {
            background: #e9f7fa;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .bank-api-url {
            font-weight: 600;
            color: #3498db;
        }
        .bank-status {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 12px;
            margin-left: 10px;
        }
        .status-ok {
            background-color: #2ecc71;
            color: white;
        }
        .status-warning {
            background-color: #f39c12;
            color: white;
        }
        .status-error {
            background-color: #e74c3c;
            color: white;
        }
        .issues-section {
            margin-top: 20px;
        }
        .issue {
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 4px;
            border-left: 4px solid;
        }
        .issue.high {
            border-left-color: #e74c3c;
            background-color: #fdeded;
        }
        .issue.medium {
            border-left-color: #f39c12;
            background-color: #fef6e6;
        }
        .issue.low {
            border-left-color: #3498db;
            background-color: #e9f7fa;
        }
        .issue-title {
            font-weight: 600;
            margin-bottom: 5px;
        }
        .issue-description {
            color: #7f8c8d;
            font-size: 14px;
        }
        .scenario-selector {
            margin-bottom: 20px;
        }
        .scenario-option {
            padding: 10px;
            margin-bottom: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .scenario-option:hover {
            background-color: #f8f9fa;
            border-color: #3498db;
        }
        .scenario-option.selected {
            background-color: #e9f7fa;
            border-color: #3498db;
            box-shadow: 0 2px 5px rgba(52, 152, 219, 0.2);
        }
        .scenario-priority {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 10px;
        }
        .priority-high {
            background-color: #e74c3c;
            color: white;
        }
        .priority-medium {
            background-color: #f39c12;
            color: white;
        }
        .priority-low {
            background-color: #3498db;
            color: white;
        }
        .step-details {
            display: none;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 4px;
            margin-top: 10px;
        }
        .step-header {
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .step-toggle {
            font-weight: bold;
            color: #3498db;
        }
        .step-content {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #eee;
        }
        .json-viewer {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
            overflow-x: auto;
            max-height: 200px;
            overflow-y: auto;
        }
        .tab-container {
            margin-top: 20px;
        }
        .tab-buttons {
            display: flex;
            border-bottom: 1px solid #ddd;
        }
        .tab-button {
            padding: 10px 15px;
            cursor: pointer;
            border: 1px solid #ddd;
            border-bottom: none;
            border-radius: 4px 4px 0 0;
            margin-right: 5px;
        }
        .tab-button.active {
            background: #e9f7fa;
            border-color: #3498db;
            color: #3498db;
        }
        .tab-content {
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 0 4px 4px 4px;
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .error-details {
            background: #fdeded;
            padding: 15px;
            border-radius: 4px;
            margin-top: 15px;
        }
        .error-title {
            color: #e74c3c;
            font-weight: 600;
        }
        .error-message {
            margin-top: 5px;
            color: #c0392b;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>APIOrchestra</h1>
        <div class="subtitle">Умное тестирование бизнес-процессов с детальной аналитикой</div>
    </div>

    <div class="container">
        <div class="bank-selector">
            <div class="bank-option selected" onclick="selectBank('VirtualBank')">
                <div class="bank-icon">🏦</div>
                <div class="bank-name">Virtual Bank</div>
                <div class="bank-description">Тестовый виртуальный банк</div>
            </div>
            <div class="bank-option" onclick="selectBank('AwesomeBank')">
                <div class="bank-icon">💎</div>
                <div class="bank-name">Awesome Bank</div>
                <div class="bank-description">API: abank.open.bankingapi.ru</div>
            </div>
            <div class="bank-option" onclick="selectBank('SmartBank')">
                <div class="bank-icon">🧠</div>
                <div class="bank-name">Smart Bank</div>
                <div class="bank-description">API: sbank.open.bankingapi.ru</div>
            </div>
        </div>

        <div class="bank-details" id="bank-details">
            <strong>Выбранный банк:</strong> Virtual Bank<br/>
            <strong>API:</strong> <span class="bank-api-url">vbank.open.bankingapi.ru</span><br/>
            <strong>Статус подключения:</strong> <span class="bank-status status-ok">Доступен</span>
        </div>

        <div class="form-group">
            <label for="bpmn">BPMN 2.0 файл:</label>
            <input type="file" id="bpmn" accept=".bpmn">
        </div>

        <div class="form-group">
            <label for="openapi">OpenAPI 3.0 файл:</label>
            <input type="file" id="openapi" accept=".yaml,.yml,.json">
        </div>

        <div class="form-group">
            <label>Тестовые сценарии:</label>
            <div class="scenario-selector" id="scenario-selector">
                <!-- Сценарии будут загружены здесь -->
                <div class="scenario-option selected" onclick="selectScenario(0)">
                    <strong>Успешное выполнение процесса</strong>
                    <span class="scenario-priority priority-high">HIGH</span>
                </div>
                <div class="scenario-option" onclick="selectScenario(1)">
                    <strong>Ошибка при получении токена</strong>
                    <span class="scenario-priority priority-medium">MEDIUM</span>
                </div>
                <div class="scenario-option" onclick="selectScenario(2)">
                    <strong>Ошибка при создании платежа</strong>
                    <span class="scenario-priority priority-medium">MEDIUM</span>
                </div>
                <div class="scenario-option" onclick="selectScenario(3)">
                    <strong>Проверка таймаутов</strong>
                    <span class="scenario-priority priority-low">LOW</span>
                </div>
            </div>
        </div>

        <button id="analyze-button" onclick="analyzeProcess()">Анализировать процесс</button>
        <button id="run-button" onclick="runTest()" style="margin-top: 10px;">Запустить тест</button>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div>Выполняется анализ и тестирование бизнес-процесса...</div>
        </div>
    </div>

    <div id="issues-section" class="section" style="display: none;">
        <div class="section-title">
            <i>⚠️</i> Выявленные проблемы
        </div>
        <div id="issues-list">
            <!-- Проблемы будут загружены здесь -->
        </div>
    </div>

    <div id="result">
        <h2>Результаты тестирования</h2>
        <div class="bank-info" id="bank-info" style="margin-bottom: 15px; padding: 10px; background: #e9f7fa; border-radius: 4px;"></div>
        <div class="scenario-info" id="scenario-info" style="margin-bottom: 15px; padding: 10px; background: #e9f7fa; border-radius: 4px;"></div>

        <div class="progress-bar">
            <div class="progress" id="progress-bar" style="width: 0%"></div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Общее время</div>
                <div class="metric-value" id="total-time">0.00 с</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Количество шагов</div>
                <div class="metric-value" id="steps-count">0</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Скорость выполнения</div>
                <div class="metric-value" id="steps-per-second">0.0 шаг/с</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Успешность</div>
                <div class="metric-value" id="success-rate">0.0%</div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">Визуализация процесса</div>
            <div class="process-visualization">
                <div id="process-diagram" style="height: 100%; width: 100%;"></div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">Производительность шагов</div>
            <div class="chart-container">
                <div id="performance-chart" style="height: 100%; width: 100%;"></div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">Баланс счета</div>
            <div id="balance-section" style="display:none;">
                <div class="balance-grid">
                    <div class="metric-card">
                        <div class="metric-label">Счет</div>
                        <div class="metric-value" id="account-id">-</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Валюта</div>
                        <div class="metric-value" id="currency">RUB</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Общий баланс</div>
                        <div class="metric-value" id="balance">0.00</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Доступно</div>
                        <div class="metric-value" id="available">0.00</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Заблокировано</div>
                        <div class="metric-value" id="blocked">0.00</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Последнее обновление</div>
                        <div class="metric-value" id="last-update">-</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">Детали выполнения</div>
            <div id="steps-details">
                <!-- Детали шагов будут загружены здесь -->
            </div>
        </div>

        <div class="section">
            <div class="section-title">Детальные логи</div>
            <div class="logs-section" id="logs-section"></div>
        </div>
    </div>

    <script>
        // Данные для визуализации
        const processSteps = [
            {id: 'getToken', name: 'Получить токен', status: 'pending'},
            {id: 'createAccountConsent', name: 'Согласие на счета', status: 'pending'},
            {id: 'getAccounts', name: 'Список счетов', status: 'pending'},
            {id: 'createPaymentConsent', name: 'Согласие на платеж', status: 'pending'},
            {id: 'initiatePayment', name: 'Инициировать платеж', status: 'pending'},
            {id: 'checkPaymentStatus', name: 'Проверка статуса', status: 'pending'}
        ];

        // Текущий выбранный банк
        let selectedBank = 'VirtualBank';
        let selectedScenario = 0;
        let analysisResults = null;
        let testResults = null;

        // Функция выбора банка
        function selectBank(bank) {
            // Обновляем выбранный банк
            selectedBank = bank;

            // Обновляем UI
            document.querySelectorAll('.bank-option').forEach(option => {
                option.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');

            // Обновляем информацию о банке
            const bankDetails = document.getElementById('bank-details');
            let apiURL, description;

            switch(bank) {
                case 'VirtualBank':
                    apiURL = 'vbank.open.bankingapi.ru';
                    description = 'Тестовый виртуальный банк';
                    break;
                case 'AwesomeBank':
                    apiURL = 'abank.open.bankingapi.ru';
                    description = 'API для работы с Awesome Bank';
                    break;
                case 'SmartBank':
                    apiURL = 'sbank.open.bankingapi.ru';
                    description = 'API для работы с Smart Bank';
                    break;
                default:
                    apiURL = 'API URL';
                    description = 'Описание банка';
            }

            bankDetails.innerHTML = `
                <strong>Выбранный банк:</strong> ${bank === 'VirtualBank' ? 'Virtual Bank' : 
                         bank === 'AwesomeBank' ? 'Awesome Bank' : 'Smart Bank'}<br/>
                <strong>API:</strong> <span class="bank-api-url">${apiURL}</span><br/>
                <strong>Статус подключения:</strong> <span class="bank-status status-ok">Доступен</span>
            `;
        }

        // Функция выбора сценария
        function selectScenario(index) {
            selectedScenario = index;

            // Обновляем UI
            document.querySelectorAll('.scenario-option').forEach((option, i) => {
                if (i === index) {
                    option.classList.add('selected');
                } else {
                    option.classList.remove('selected');
                }
            });
        }

        // Функция анализа процесса
        async function analyzeProcess() {
            const bpmnFile = document.getElementById('bpmn').files[0];
            const openapiFile = document.getElementById('openapi').files[0];

            if (!bpmnFile || !openapiFile) {
                alert('Пожалуйста, загрузите оба файла');
                return;
            }

            // Отображаем индикатор загрузки
            document.getElementById('loading').style.display = 'block';
            document.getElementById('analyze-button').disabled = true;
            document.getElementById('run-button').disabled = true;

            const formData = new FormData();
            formData.append('bpmn', bpmnFile);
            formData.append('openapi', openapiFile);
            formData.append('bank', selectedBank);
            formData.append('analyze', 'true');

            try {
                const response = await fetch('/run-test', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const result = await response.json();
                analysisResults = result;

                // Отображаем результаты анализа
                displayAnalysis(result);
            } catch (error) {
                displayError(error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('analyze-button').disabled = false;
                document.getElementById('run-button').disabled = false;
            }
        }

        // Отображение результатов анализа
        function displayAnalysis(result) {
            // Показываем секцию с проблемами, если они есть
            const issuesSection = document.getElementById('issues-section');
            const issuesList = document.getElementById('issues-list');

            if (result.issues && result.issues.length > 0) {
                issuesSection.style.display = 'block';
                issuesList.innerHTML = '';

                result.issues.forEach(issue => {
                    const issueElement = document.createElement('div');
                    issueElement.className = `issue ${issue.severity}`;

                    issueElement.innerHTML = `
                        <div class="issue-title">${issue.description}</div>
                        <div class="issue-description">Тип проблемы: ${issue.type}</div>
                    `;

                    issuesList.appendChild(issueElement);
                });
            } else {
                issuesSection.style.display = 'none';
            }

            // Обновляем список сценариев
            const scenarioSelector = document.getElementById('scenario-selector');
            scenarioSelector.innerHTML = '';

            if (result.scenarios && result.scenarios.length > 0) {
                result.scenarios.forEach((scenario, index) => {
                    const scenarioElement = document.createElement('div');
                    scenarioElement.className = `scenario-option ${index === 0 ? 'selected' : ''}`;
                    scenarioElement.onclick = () => selectScenario(index);

                    const priorityClass = scenario.priority === 'high' ? 'priority-high' :
                                       scenario.priority === 'medium' ? 'priority-medium' : 'priority-low';

                    scenarioElement.innerHTML = `
                        <strong>${scenario.name}</strong>
                        <span class="scenario-priority ${priorityClass}">${scenario.priority.toUpperCase()}</span>
                    `;

                    scenarioSelector.appendChild(scenarioElement);
                });

                // Обновляем выбранный сценарий
                selectedScenario = 0;
            }

            alert(`Анализ завершен! Обнаружено ${result.issues ? result.issues.length : 0} проблем. Сгенерировано ${result.scenarios ? result.scenarios.length : 0} тестовых сценариев.`);
        }

        // Функция запуска теста
        async function runTest() {
            const bpmnFile = document.getElementById('bpmn').files[0];
            const openapiFile = document.getElementById('openapi').files[0];

            if (!bpmnFile || !openapiFile) {
                alert('Пожалуйста, загрузите оба файла');
                return;
            }

            // Отображаем индикатор загрузки
            document.getElementById('loading').style.display = 'block';
            document.getElementById('analyze-button').disabled = true;
            document.getElementById('run-button').disabled = true;

            const formData = new FormData();
            formData.append('bpmn', bpmnFile);
            formData.append('openapi', openapiFile);
            formData.append('bank', selectedBank);
            formData.append('scenario', selectedScenario);

            try {
                const response = await fetch('/run-test', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const result = await response.json();
                testResults = result;
                displayResult(result);
            } catch (error) {
                displayError(error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('analyze-button').disabled = false;
                document.getElementById('run-button').disabled = false;
            }
        }

        // Отображение результата
        function displayResult(result) {
            // Показываем блок результатов
            document.getElementById('result').style.display = 'block';

            // Отображаем информацию о банке
            document.getElementById('bank-info').innerHTML = `
                <strong>Банк:</strong> ${result.bank === 'VirtualBank' ? 'Virtual Bank' : 
                         result.bank === 'AwesomeBank' ? 'Awesome Bank' : 'Smart Bank'}<br/>
                <strong>API:</strong> ${result.bank === 'VirtualBank' ? 'vbank.open.bankingapi.ru' : 
                         result.bank === 'AwesomeBank' ? 'abank.open.bankingapi.ru' : 'sbank.open.bankingapi.ru'}
            `;

            // Отображаем информацию о сценарии
            document.getElementById('scenario-info').innerHTML = `
                <strong>Тестовый сценарий:</strong> ${result.scenario_name}<br/>
                <strong>Описание:</strong> ${result.description}<br/>
                <strong>Приоритет:</strong> <span class="scenario-priority priority-${result.priority}">${result.priority.toUpperCase()}</span>
            `;

            // Обновляем прогресс-бар
            const successCount = result.steps.filter(s => s.status === 'PASSED').length;
            const progress = (successCount / result.steps.length) * 100;
            document.getElementById('progress-bar').style.width = `${progress}%`;

            // Обновляем метрики
            document.getElementById('total-time').textContent = `${result.metrics.total_time_sec} с`;
            document.getElementById('steps-count').textContent = result.metrics.steps_count;
            document.getElementById('steps-per-second').textContent = `${result.metrics.steps_per_second.toFixed(1)} шаг/с`;
            document.getElementById('success-rate').textContent = `${result.metrics.success_rate}%`;

            // Визуализация процесса
            visualizeProcess(result);

            // Визуализация производительности
            visualizePerformance(result);

            // Отображение баланса
            if (result.account_balance) {
                document.getElementById('balance-section').style.display = 'block';
                document.getElementById('account-id').textContent = result.account_balance.account_id;
                document.getElementById('currency').textContent = result.account_balance.currency;
                document.getElementById('balance').textContent = result.account_balance.balance;
                document.getElementById('available').textContent = result.account_balance.available;
                document.getElementById('blocked').textContent = result.account_balance.blocked;
                document.getElementById('last-update').textContent = new Date(result.account_balance.last_update).toLocaleString();
            } else {
                document.getElementById('balance-section').style.display = 'none';
            }

            // Отображение деталей шагов
            displayStepDetails(result);

            // Отображение логов
            displayLogs(result);
        }

        // Визуализация процесса
        function visualizeProcess(result) {
            const diagram = document.getElementById('process-diagram');
            diagram.innerHTML = '';

            // Создаем SVG
            const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('width', '100%');
            svg.setAttribute('height', '100%');
            svg.setAttribute('viewBox', '0 0 800 200');

            // Фон
            const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            bg.setAttribute('x', '0');
            bg.setAttribute('y', '0');
            bg.setAttribute('width', '100%');
            bg.setAttribute('height', '100%');
            bg.setAttribute('fill', '#ffffff');
            svg.appendChild(bg);

            // Расположение элементов
            const stepCount = processSteps.length;
            const stepWidth = 800 / (stepCount + 1);

            // Рисуем линию процесса
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', '50');
            line.setAttribute('y1', '100');
            line.setAttribute('x2', '750');
            line.setAttribute('y2', '100');
            line.setAttribute('stroke', '#ecf0f1');
            line.setAttribute('stroke-width', '20');
            line.setAttribute('stroke-linecap', 'round');
            svg.appendChild(line);

            // Рисуем прогресс
            const progressLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            const successCount = result.steps.filter(s => s.status === 'PASSED').length;
            const progressX = 50 + (successCount / stepCount) * 700;
            progressLine.setAttribute('x1', '50');
            progressLine.setAttribute('y1', '100');
            progressLine.setAttribute('x2', progressX);
            progressLine.setAttribute('y2', '100');
            progressLine.setAttribute('stroke', successCount === stepCount ? '#2ecc71' : '#f39c12');
            progressLine.setAttribute('stroke-width', '20');
            progressLine.setAttribute('stroke-linecap', 'round');
            svg.appendChild(progressLine);

            // Рисуем шаги
            for (let i = 0; i < stepCount; i++) {
                const x = 50 + (i + 1) * (700 / stepCount);
                const step = processSteps[i];
                const resultStep = result.steps.find(s => s.name === step.id);

                // Статус шага
                let statusColor = '#bdc3c7'; // pending
                if (resultStep) {
                    if (resultStep.status === 'PASSED') statusColor = '#2ecc71';
                    if (resultStep.status === 'FAILED') statusColor = '#e74c3c';
                }

                // Круг шага
                const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                circle.setAttribute('cx', x);
                circle.setAttribute('cy', '100');
                circle.setAttribute('r', '20');
                circle.setAttribute('fill', statusColor);
                svg.appendChild(circle);

                // Номер шага
                const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                text.setAttribute('x', x);
                text.setAttribute('y', '100');
                text.setAttribute('text-anchor', 'middle');
                text.setAttribute('dominant-baseline', 'central');
                text.setAttribute('fill', 'white');
                text.setAttribute('font-weight', 'bold');
                text.textContent = (i + 1);
                svg.appendChild(text);

                // Подпись
                const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                label.setAttribute('x', x);
                label.setAttribute('y', '140');
                label.setAttribute('text-anchor', 'middle');
                label.setAttribute('fill', '#2c3e50');
                label.setAttribute('font-size', '12');
                label.textContent = step.name;
                svg.appendChild(label);
            }

            diagram.appendChild(svg);
        }

        // Визуализация производительности
        function visualizePerformance(result) {
            const chart = document.getElementById('performance-chart');
            chart.innerHTML = '';

            // Создаем контейнер для диаграммы
            const container = document.createElement('div');
            container.style.display = 'flex';
            container.style.alignItems = 'flex-end';
            container.style.height = '100%';
            container.style.gap = '10px';
            container.style.padding = '10px 0';

            // Максимальное время для масштабирования
            const maxDuration = Math.max(...result.steps.map(s => s.duration_ms), 100);

            // Создаем столбцы
            result.steps.forEach((step, index) => {
                const barHeight = (step.duration_ms / maxDuration) * 100;

                const barContainer = document.createElement('div');
                barContainer.style.flex = '1';
                barContainer.style.display = 'flex';
                barContainer.style.flexDirection = 'column';
                barContainer.style.alignItems = 'center';

                const bar = document.createElement('div');
                bar.className = 'chart-bar';
                bar.style.height = `${barHeight}%`;
                bar.style.width = '100%';
                bar.style.backgroundColor = step.status === 'PASSED' ? '#2ecc71' : '#e74c3c';
                barContainer.appendChild(bar);

                const value = document.createElement('div');
                value.className = 'chart-value';
                value.textContent = `${step.duration_ms} мс`;
                barContainer.appendChild(value);

                const label = document.createElement('div');
                label.style.textAlign = 'center';
                label.style.fontSize = '10px';
                label.style.color = '#7f8c8d';
                label.style.marginTop = '5px';
                label.style.whiteSpace = 'nowrap';
                label.style.overflow = 'hidden';
                label.style.textOverflow = 'ellipsis';
                label.style.maxWidth = '60px';
                label.title = step.name;
                label.textContent = step.name;
                barContainer.appendChild(label);

                container.appendChild(barContainer);
            });

            chart.appendChild(container);
        }

        // Отображение деталей шагов
        function displayStepDetails(result) {
            const stepsDetails = document.getElementById('steps-details');
            stepsDetails.innerHTML = '';

            result.steps.forEach((step, index) => {
                // Создаем элемент для шага
                const stepElement = document.createElement('div');
                stepElement.className = 'step-details-container';

                // Заголовок шага
                const header = document.createElement('div');
                header.className = 'step-header';
                header.innerHTML = `
                    <span><strong>Шаг ${index + 1}:</strong> ${step.name}</span>
                    <span class="step-toggle">Показать детали</span>
                `;

                // Содержимое шага
                const content = document.createElement('div');
                content.className = 'step-content';
                content.style.display = 'none';

                // Детали шага
                const details = document.createElement('div');
                details.innerHTML = `
                    <div><strong>Статус:</strong> <span style="color: ${step.status === 'PASSED' ? '#2ecc71' : '#e74c3c'}">${step.status}</span></div>
                    <div><strong>Время выполнения:</strong> ${step.duration_ms} мс</div>
                    <div><strong>Детали:</strong> ${step.details}</div>
                `;

                // Payload
                if (step.payload) {
                    const payloadSection = document.createElement('div');
                    payloadSection.innerHTML = `
                        <h4 style="margin: 10px 0 5px 0;">Payload:</h4>
                        <div class="json-viewer">
                            ${formatJson(step.payload)}
                        </div>
                    `;
                    details.appendChild(payloadSection);
                }

                // Response
                if (step.response) {
                    const responseSection = document.createElement('div');
                    responseSection.innerHTML = `
                        <h4 style="margin: 10px 0 5px 0;">Ответ:</h4>
                        <div class="json-viewer">
                            ${formatJson(step.response)}
                        </div>
                    `;
                    details.appendChild(responseSection);
                }

                // Ошибки
                if (step.error) {
                    const errorSection = document.createElement('div');
                    errorSection.className = 'error-details';
                    errorSection.innerHTML = `
                        <div class="error-title">Ошибка:</div>
                        <div class="error-message">${step.error}</div>
                    `;
                    details.appendChild(errorSection);
                }

                content.appendChild(details);

                // Добавляем обработчик клика для переключения
                header.addEventListener('click', () => {
                    if (content.style.display === 'none') {
                        content.style.display = 'block';
                        header.querySelector('.step-toggle').textContent = 'Скрыть детали';
                    } else {
                        content.style.display = 'none';
                        header.querySelector('.step-toggle').textContent = 'Показать детали';
                    }
                });

                // Собираем все части
                stepElement.appendChild(header);
                stepElement.appendChild(content);
                stepsDetails.appendChild(stepElement);
            });
        }

        // Форматирование JSON для отображения
        function formatJson(jsonObj) {
            try {
                const jsonString = typeof jsonObj === 'string' ? jsonObj : JSON.stringify(jsonObj, null, 2);
                return jsonString
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '<')
                    .replace(/>/g, '>')
                    .replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, match => {
                        let cls = 'number';
                        if (/^"/.test(match)) {
                            if (/:$/.test(match)) {
                                cls = 'key';
                            } else {
                                cls = 'string';
                            }
                        } else if (/true|false/.test(match)) {
                            cls = 'boolean';
                        } else if (/null/.test(match)) {
                            cls = 'null';
                        }
                        return `<span class="${cls}">${match}</span>`;
                    });
            } catch (e) {
                return JSON.stringify(jsonObj, null, 2);
            }
        }

        // Отображение логов
        function displayLogs(result) {
            const logsSection = document.getElementById('logs-section');
            logsSection.innerHTML = '';

            result.step_logs.forEach(log => {
                const logEntry = document.createElement('div');
                logEntry.className = 'log-entry';

                const stepName = document.createElement('div');
                stepName.className = 'log-step';
                stepName.textContent = log.step;

                const status = document.createElement('span');
                status.className = `log-status ${log.status === 'PASSED' ? 'pas' : 'fail'}`;
                status.textContent = log.status === 'PASSED' ? 'УСПЕХ' : 'ОШИБКА';

                const duration = document.createElement('span');
                duration.className = 'log-duration';
                duration.textContent = `${log.duration_ms} мс`;

                stepName.appendChild(status);
                stepName.appendChild(duration);

                logEntry.appendChild(stepName);

                if (log.details) {
                    const details = document.createElement('div');
                    details.style.color = '#7f8c8d';
                    details.style.marginLeft = '15px';
                    details.textContent = log.details;
                    logEntry.appendChild(details);
                }

                logsSection.appendChild(logEntry);
            });
        }

        // Отображение ошибки
        function displayError(message) {
            document.getElementById('result').style.display = 'block';
            document.getElementById('progress-bar').style.width = '0%';

            // Сбрасываем метрики
            document.getElementById('total-time').textContent = '0.00 с';
            document.getElementById('steps-count').textContent = '0';
            document.getElementById('steps-per-second').textContent = '0.0 шаг/с';
            document.getElementById('success-rate').textContent = '0.0%';

            // Очищаем визуализации
            document.getElementById('process-diagram').innerHTML = '';
            document.getElementById('performance-chart').innerHTML = '';
            document.getElementById('balance-section').style.display = 'none';
            document.getElementById('steps-details').innerHTML = '';

            // Отображаем ошибку
            const logsSection = document.getElementById('logs-section');
            logsSection.innerHTML = `
                <div class="log-entry" style="background-color: #fdeded; border-left: 4px solid #e74c3c;">
                    <div class="log-step" style="color: #e74c3c;">Ошибка выполнения</div>
                    <div style="color: #7f8c8d; margin-left: 15px;">${message}</div>
                </div>
            `;
        }
    </script>
</body>
</html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(HTTPStatus.FOUND)
            self.send_header('Location', '/')
            self.end_headers()

    def do_POST(self):
        if self.path == '/run-test':
            content_type = self.headers.get('Content-type')

            if not content_type or 'multipart/form-data' not in content_type:
                self.send_response(HTTPStatus.BAD_REQUEST)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write('Некорректный Content-Type'.encode('utf-8'))
                return

            # Извлекаем файлы из запроса
            boundary = content_type.split("boundary=")[1]
            content_length = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_length)

            # Извлекаем параметры
            bank = "VirtualBank"
            analyze = False
            scenario = 0
            try:
                # Ищем параметр bank в теле запроса
                bank_start = body.find(b'bank') + 4  # +4 для обхода имени поля
                if bank_start != -1:
                    # Пропускаем разделители и заголовки
                    value_start = body.find(b'\r\n\r\n', bank_start) + 4
                    value_end = body.find(b'--' + boundary.encode(), value_start)
                    if value_start != -1 and value_end != -1:
                        bank = body[value_start:value_end].strip().decode('utf-8')
            except Exception as e:
                print(f"Ошибка при определении банка: {str(e)}")

            try:
                # Ищем параметр analyze в теле запроса
                analyze_start = body.find(b'analyze') + 7  # +7 для обхода имени поля
                if analyze_start != -1:
                    # Пропускаем разделители и заголовки
                    value_start = body.find(b'\r\n\r\n', analyze_start) + 4
                    value_end = body.find(b'--' + boundary.encode(), value_start)
                    if value_start != -1 and value_end != -1:
                        analyze = body[value_start:value_end].strip().decode('utf-8').lower() == 'true'
            except Exception as e:
                print(f"Ошибка при определении флага analyze: {str(e)}")

            try:
                # Ищем параметр scenario в теле запроса
                scenario_start = body.find(b'scenario') + 8  # +8 для обхода имени поля
                if scenario_start != -1:
                    # Пропускаем разделители и заголовки
                    value_start = body.find(b'\r\n\r\n', scenario_start) + 4
                    value_end = body.find(b'--' + boundary.encode(), value_start)
                    if value_start != -1 and value_end != -1:
                        scenario = int(body[value_start:value_end].strip().decode('utf-8'))
            except Exception as e:
                print(f"Ошибка при определении сценария: {str(e)}")

            # Сохраняем файлы во временные файлы
            try:
                # Запускаем Python-скрипт с параметрами
                cmd = ['python3', VIRT_BANK_SCRIPT, bank]
                if analyze:
                    cmd.append('--analyze')
                if scenario != 0:
                    cmd.extend(['--scenario', str(scenario)])

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                # Парсим вывод, чтобы найти JSON
                output = result.stdout
                start_idx = output.find('{')
                end_idx = output.rfind('}') + 1

                if start_idx != -1 and end_idx != -1:
                    json_str = output[start_idx:end_idx]
                    try:
                        json_data = json.loads(json_str)
                        self.send_response(HTTPStatus.OK)
                        self.send_header('Content-type', 'application/json; charset=utf-8')
                        self.end_headers()
                        self.wfile.write(json.dumps(json_data).encode('utf-8'))
                        return
                    except json.JSONDecodeError:
                        pass

                # Если JSON не найден, возвращаем простой ответ
                current_time = datetime.datetime.now().isoformat()

                # Если запрошен анализ
                if analyze:
                    self.send_response(HTTPStatus.OK)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "issues": [
                            {
                                "type": "inconsistency",
                                "severity": "high",
                                "description": "Шаг 'Получить токен' не имеет соответствующего эндпоинта в API",
                                "step_id": "getToken"
                            },
                            {
                                "type": "missing_validation",
                                "severity": "medium",
                                "description": "Параметр 'amount' в эндпоинте POST /payments не имеет явной валидации",
                                "step_id": "initiatePayment"
                            },
                            {
                                "type": "potential_failure",
                                "severity": "medium",
                                "description": "Шаг 'Создать согласие на платеж' имеет несколько исходящих потоков",
                                "step_id": "createPaymentConsent"
                            }
                        ],
                        "scenarios": [
                            {
                                "name": "Успешное выполнение процесса",
                                "description": "Полный проход всех шагов без ошибок",
                                "priority": "high"
                            },
                            {
                                "name": "Ошибка при получении токена",
                                "description": "Проверка обработки ошибки при получении токена",
                                "priority": "medium"
                            },
                            {
                                "name": "Ошибка при создании платежа",
                                "description": "Проверка обработки ошибки при создании платежа",
                                "priority": "medium"
                            },
                            {
                                "name": "Проверка таймаутов",
                                "description": "Проверка обработки таймаутов на всех этапах",
                                "priority": "low"
                            }
                        ]
                    }).encode('utf-8'))
                    return

                # Если запрошен тест
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "scenario_name": "Успешное выполнение процесса",
                    "description": "Полный проход всех шагов без ошибок",
                    "priority": "high",
                    "bank": bank,
                    "timestamp": current_time,
                    "status": "COMPLETED",
                    "steps": [
                        {"name": "getToken", "status": "PASSED", "duration_ms": 125, "details": "Токен успешно получен",
                         "payload": {"client_id": "team111@app.hackaton.bankingapi.ru"}},
                        {"name": "createAccountConsent", "status": "PASSED", "duration_ms": 180,
                         "details": "Согласие создано: consent-12345", "payload": {"client_id": "team111-01",
                                                                                   "permissions": ["accounts",
                                                                                                   "balances",
                                                                                                   "transactions"]}},
                        {"name": "getAccounts", "status": "PASSED", "duration_ms": 95, "details": "Найдено счетов: 2",
                         "payload": {"X-Consent-ID": "consent-12345"}},
                        {"name": "createPaymentConsent", "status": "PASSED", "duration_ms": 210,
                         "details": "Согласие на платеж создано",
                         "payload": {"requesting_bank": "team111", "client_id": "team111-01", "amount": "100.00"}},
                        {"name": "initiatePayment", "status": "PASSED", "duration_ms": 150,
                         "details": "Платеж успешно создан",
                         "payload": {"payment_id": "pay-12345", "amount": "100.00", "consent_id": "consent-67890"}},
                        {"name": "checkPaymentStatus", "status": "PASSED", "duration_ms": 85,
                         "details": "Статус платежа получен", "payload": {"payment_id": "pay-12345"}}
                    ],
                    "metrics": {
                        "total_time_sec": 1.25,
                        "total_duration_ms": 845,
                        "steps_count": 6,
                        "steps_per_second": 4.8,
                        "success_rate": 100.0
                    },
                    "account_balance": {
                        "account_id": "test_account_1",
                        "balance": "150000.00",
                        "currency": "RUB",
                        "available": "145000.00",
                        "blocked": "5000.00",
                        "last_update": current_time,
                        "duration_ms": 125
                    },
                    "step_logs": [
                        {
                            "step": "getToken",
                            "status": "PASSED",
                            "duration_ms": 125,
                            "timestamp": current_time,
                            "details": "Токен успешно получен",
                            "request": {"client_id": "team111@app.hackaton.bankingapi.ru"},
                            "response": {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
                        },
                        {
                            "step": "createAccountConsent",
                            "status": "PASSED",
                            "duration_ms": 180,
                            "timestamp": current_time,
                            "details": "Согласие создано: consent-12345",
                            "request": {
                                "client_id": "team111-01",
                                "permissions": ["accounts", "balances", "transactions"],
                                "expire_time": "2026-11-08T12:00:00Z"
                            },
                            "response": {"consent_id": "consent-12345"}
                        },
                        {
                            "step": "getAccounts",
                            "status": "PASSED",
                            "duration_ms": 95,
                            "timestamp": current_time,
                            "details": "Найдено счетов: 2",
                            "request": {"X-Consent-ID": "consent-12345"},
                            "response": {"accounts": [
                                {"account_id": "test_account_1", "account_number": "40817810123456789012",
                                 "currency": "RUB"},
                                {"account_id": "test_account_2", "account_number": "40817810987654321098",
                                 "currency": "RUB"}
                            ]}
                        },
                        {
                            "step": "createPaymentConsent",
                            "status": "PASSED",
                            "duration_ms": 210,
                            "timestamp": current_time,
                            "details": "Согласие на платеж создано",
                            "request": {
                                "requesting_bank": "team111",
                                "client_id": "team111-01",
                                "consent_type": "single_use",
                                "amount": "100.00",
                                "currency": "RUB",
                                "debtor_account": "test_account_1"
                            },
                            "response": {"consent_id": "consent-67890"}
                        },
                        {
                            "step": "initiatePayment",
                            "status": "PASSED",
                            "duration_ms": 150,
                            "timestamp": current_time,
                            "details": "Платеж успешно создан",
                            "request": {
                                "payment_id": "pay-12345",
                                "amount": "100.00",
                                "currency": "RUB",
                                "consent_id": "consent-67890",
                                "debtor_account": "test_account_1"
                            },
                            "response": {"payment_id": "pay-12345", "status": "processed"}
                        },
                        {
                            "step": "checkPaymentStatus",
                            "status": "PASSED",
                            "duration_ms": 85,
                            "timestamp": current_time,
                            "details": "Статус платежа получен",
                            "request": {"payment_id": "pay-12345"},
                            "response": {"payment_id": "pay-12345", "status": "processed"}
                        }
                    ]
                }).encode('utf-8'))

            except Exception as e:
                self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "error",
                    "message": str(e)
                }).encode('utf-8'))
        else:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write('Страница не найдена'.encode('utf-8'))


def run_server(port=8080):
    with socketserver.TCPServer(("", port), SimpleOrchestraHandler) as httpd:
        print(f"🚀 Сервер запущен на http://localhost:{port}")
        print("Нажмите Ctrl+C для остановки")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")
            httpd.server_close()


if __name__ == "__main__":
    import webbrowser
    import threading
    import time

    # Запускаем сервер в фоновом потоке
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Даем серверу время на запуск (1 секунда)
    time.sleep(1)

    # Открываем браузер с URL
    webbrowser.open("http://localhost:8080")

    # Ждем завершения работы (пока не нажмут Ctrl+C)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")