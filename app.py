from flask import Flask, request, jsonify, abort
import os

app = Flask(__name__)

# Пример токена доступа для администраторов
ADMIN_TOKENS = {
    'admin_token_1': 'chat_id_1',
    'admin_token_2': 'chat_id_2'
}

# Функция для проверки токена доступа
def verify_token(token):
    return ADMIN_TOKENS.get(token)

# Функция для создания или обновления файла рангов
def update_ranks_file(chat_id, ranks):
    file_path = os.path.join('rank_module', f'ranks_{chat_id}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        for rank in ranks:
            file.write(f"{rank}\n")

# Функция для создания или обновления файла опыта
def update_experience_file(chat_id, experience_thresholds):
    file_path = os.path.join('rank_module', f'experience_{chat_id}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        for experience in experience_thresholds:
            file.write(f"{experience}\n")

@app.route('/api/ranks/<int:chat_id>', methods=['POST'])
def update_ranks(chat_id):
    token = request.headers.get('Authorization')
    if not token or not verify_token(token):
        abort(403)
    data = request.json
    ranks = data.get('ranks', [])
    update_ranks_file(chat_id, ranks)
    return jsonify({"message": "Ranks updated successfully"})

@app.route('/api/experience/<int:chat_id>', methods=['POST'])
def update_experience(chat_id):
    token = request.headers.get('Authorization')
    if not token or not verify_token(token):
        abort(403)
    data = request.json
    experience_thresholds = data.get('experience_thresholds', [])
    update_experience_file(chat_id, experience_thresholds)
    return jsonify({"message": "Experience thresholds updated successfully"})

if __name__ == '__main__':
    app.run(debug=True)
