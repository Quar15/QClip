function hideElement(el) {
    el.classList.add("hidden");
}

function linkHandlingTitleFromFileUpload() {
    const UPLOAD_VIDEO_FORM = document.querySelector("#upload-popover form");
    const UPLOAD_VIDEO_FORM_TITLE = UPLOAD_VIDEO_FORM.querySelector("input[type='text']");
    const UPLOAD_VIDEO_FORM_FILE = UPLOAD_VIDEO_FORM.querySelector("input[type='file']");
    
    UPLOAD_VIDEO_FORM_FILE.addEventListener('change', ()=> {
        let uploadFormValue = UPLOAD_VIDEO_FORM_TITLE.value.trim();
        if (uploadFormValue != null && uploadFormValue != "") {
            console.log(uploadFormValue)
            return;
        }
        let fileName = UPLOAD_VIDEO_FORM_FILE.files[0].name;
        fileName = fileName.replace(/[^a-z0-9áéíóúñü \.,_-]/gim,"");
        fileName = fileName.replace(/\.[^/.]+$/, "");
        fileName = fileName.trim()
        UPLOAD_VIDEO_FORM_TITLE.value = fileName;
    });
}