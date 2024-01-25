function sendToRasa() {
    var userInput = document.getElementById("userInput").value;

    fetch('http://localhost:5005/model/parse', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: userInput })
    })
    .then(response => response.json())
    .then(data => displayResult(data, userInput))
    .catch(error => console.error('Error:', error));
}

function displayResult(data, userInput) {
    var responseDiv = document.getElementById("response");
    var tokensHtml = getTokensHtml(userInput, data.text_tokens, data.entities);

    responseDiv.innerHTML = `<strong class="item-name">Tokenize and Entities:</strong> <div class="tokens">${tokensHtml}</div>`;
    responseDiv.innerHTML += `<strong class="item-name">Intent:</strong> <span class="intent-name">${data.intent ? data.intent.name : "None"}</span>`;
}

function getTokensHtml(userInput, textTokens, entities) {
    var result = "";
    var currentPos = 0;

    // 先将实体按照开始位置排序，确保顺序
    entities.sort((a, b) => a.start - b.start);

    // 遍历实体，并构建高亮显示的实体和普通 token
    entities.forEach(entity => {
        // 添加实体之前的普通 token
        result += addNonEntityTokens(userInput.substring(currentPos, entity.start), textTokens);
        // 添加实体高亮部分
        result += `<span class="entity-token">${userInput.substring(entity.start, entity.end)} <span class="entity-name">[${entity.entity}]</span></span>`;
        currentPos = entity.end;
    });

    // 添加最后一个实体后的所有普通 token
    result += addNonEntityTokens(userInput.substring(currentPos), textTokens);

    return result;
}

// 用于添加非实体 token 的函数
function addNonEntityTokens(substring, textTokens) {
    return substring
      .split(/\s+/) // 分割空格
      .filter(token => token.length > 0) // 过滤空字符串
      .map(token => `<span class="token">${token}</span>`) // 将每个 token 包装在 span 中
      .join(' '); // 用空格连接
}
