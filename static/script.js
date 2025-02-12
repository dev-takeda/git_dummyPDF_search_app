document.addEventListener("DOMContentLoaded", function () {
    const filterButtons = document.querySelectorAll(".filter-btn");
    const resultsContainer = document.getElementById("search-results");
    const searchButton = document.getElementById("search-btn");
    const searchInput = document.getElementById("search-input");

    // 科目区分・タグボタンをクリックしたときの処理
    filterButtons.forEach(button => {
        button.addEventListener("click", function () {
            // すべてのボタンの active クラスを削除
            filterButtons.forEach(btn => btn.classList.remove("active"));

            // クリックされたボタンに active クラスを追加
            this.classList.add("active");

            const type = this.getAttribute("data-type");  // "subject" または "tag"
            const value = this.getAttribute("data-value");

            fetch(`/get_pdfs?type=${type}&value=${encodeURIComponent(value)}`)
                .then(response => response.json())
                .then(data => {
                    resultsContainer.innerHTML = "";  // クリア
                    if (data.length === 0) {
                        resultsContainer.innerHTML = "<p>該当する資料がありません。</p>";
                    } else {
                        data.forEach(pdf => {
                            const pdfElement = document.createElement("div");
                            pdfElement.classList.add("pdf-item");
                            pdfElement.innerHTML = `
                                <a href="/pdf/${encodeURIComponent(pdf)}" target="_blank">${pdf}</a>
                            `;
                            resultsContainer.appendChild(pdfElement);
                        });
                    }
                })
                .catch(error => console.error("Error fetching PDFs:", error));
        });
    });


    // キーワード検索の処理
    searchButton.addEventListener("click", function () {
        const keyword = searchInput.value.trim();
        if (keyword === "") {
            alert("キーワードを入力してください。");
            return;
        }

        fetch(`/search_pdfs?keyword=${encodeURIComponent(keyword)}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = "";  // クリア
                if (data.length === 0) {
                    resultsContainer.innerHTML = "<p>該当する資料がありません。</p>";
                } else {
                    data.forEach(pdf => {
                        const pdfElement = document.createElement("div");
                        pdfElement.classList.add("pdf-item");
                        pdfElement.innerHTML = `
                            <a href="/pdf/${encodeURIComponent(pdf)}" target="_blank">${pdf}</a>
                        `;
                        resultsContainer.appendChild(pdfElement);
                    });
                }
            })
            .catch(error => console.error("Error searching PDFs:", error));
    });
});

