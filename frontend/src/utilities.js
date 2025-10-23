export function fetchedDocumentsProcess(documentsObj) {
    /*It takes fetched documents objected and process it to list of documents */
    const keys = Object.keys(documentsObj);
    const length = documentsObj['ids'].length; 
    const documentsList = Array.from({ length: length }, (_, i) =>
    keys.reduce((obj, key) => {
        obj[key] = (documentsObj[key] && documentsObj[key][i]) || null;
        return obj;
    }, {})
    );

    return documentsList;
}