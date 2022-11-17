let ReviewsData = null;

function storeReviewsData(data) {
    return new Promise((complete) => {
        analyticsData = data
        complete(true)
    })
}

function getAnalyticsData(url) {
    $('#loading-modal').modal('show')
    return new Promise((complete) => {
        $.ajax({
            'url': url,
            success: async function (response) {
                if (await storeReviewsData(response["response"])) {
                    setChart(getCurrentChartType(), getDataLevelView())
                    complete(true)
                } else {
                    await alertAction("An error occurred while storing the analytics data.")
                    setTimeout(() => {
                        closeModal('loading-modal')
                    }, 500)
                    complete(false)
                }
            }
        });
    })
}

function closeModal(modalName){
	$(`#${modalName}`).modal('hide')
}

function backendCall(url, method, data) {
	return new Promise((promisedResponse) => {
		if (method !== "GET") {
			$.ajax({
				"url": url,
				"method": method,
				"dataType": "json",
				"contentType": "application/json",
				"data": JSON.stringify(data),
				success: function(response) {promisedResponse(response)}
			})
		} else {
			$.ajax({"url": url, success: function(response) {promisedResponse(response)}})
		}
	})
}

function getCachedData() {
    return backendCall('/get_cached_reviews', 'GET', null)
}

async function displayNumReturned(numEntries) {
    $('#numEntriesReturned').text(numEntries + ' Reviews Loaded');
    return;
}

async function displayData(){
    const allReviewsData = await backendCall('/get_cached_reviews', 'GET', null);
    $('review-list-table').empty()
    $('reviews-table-header').empty()

    // build out the whole table here in `<>` format and then return it so it's reusable.
    addReviewsTableHeaders();
    allReviewsData.forEach(function (reviewObj) {
        $('#review-list-table').append(addRetrainingEntry2(reviewObj));
    })
    return;
}

function addReviewsTableHeaders() {
    // const view_list = {
    //     "review_id" : "Review ID",
    //     "full_review_text" : "Text",
    // }
    const headers = ["Review ID", "Text"]
    headers.forEach((name) => {
        $('#reviews-table-header').append(`<th scope="col">${name}</th>`)
    })
}

function addReviewsList(reviewsList) {
    reviewsList.forEach((reviewText) => {
        $('#review-table-body').append(addRetrainingEntry2(review_text));
    })
}

function addRetrainingEntry(data) {
    return `<div class="card" id="card_${data.entry_id}">`
        + `<div class="card-body" id="${data.entry_id}-text">${data.entry_text}</div>`
        +`</div>`
}

function addRetrainingEntry2(review) {
    return `<tr><th scope="row">${review.review_id}</th><td>${review.full_review_text}</tr>`//`<tr><td>${data.entry_id}</td><td>${data.entry_text}</tr>`
}
