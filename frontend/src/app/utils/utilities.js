import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";


export function fetchedDocumentsProcess(documentsObj) {
    /*It takes fetched documents objected and process it to list of documents */
    const keys = Object.keys(documentsObj);
    const length = documentsObj['ids'].length; 
    const documentsList = Array.from({ length: length }, (document, idx) => {
        keys.forEach(key => {
            document = document || {};
            document[key] = (documentsObj[key] && documentsObj[key][idx]) || null;

        });
        return document;
    }
    );
    return documentsList;
}


export function queriedDocumentsProcess(documentsObj) {
    /*It takes documents resulted from query objected and process it to list of documents */
    const keys = Object.keys(documentsObj);
    const length = documentsObj['ids'][0].length; 
    const documentsList = Array.from({ length: length }, (document, idx) => {
        keys.forEach(key => {
            document = document || {};
            document[key] = (documentsObj[key] && documentsObj[key][0][idx]) || null;

        });
        return document;
    }
    );
    return documentsList;
}


export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
