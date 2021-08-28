function translate(sourceElem, destElem, sourceLang, destLang="en") {
    $(destElem).html(`<img src="{{ url_for('static', filename='loading.gif') }}">`);
    $.post("/translate", {
        text: $(sourceElem).text(),
        source_language: sourceLang,
        dest_language: destLang
    }).done(function(response) {
        $(destElem).text(response["text"]);
    }).fail(function() {
        $(destElem).text("Error: Could not contact server.");
    });
}
