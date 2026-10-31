// Google Apps Script: ask.html ফর্ম → Google Sheet (ফ্রি)
// Sheet এর প্রথম সারিতে হেডার: time, name, phone, location, floors, stage, question, source
const SHEET_NAME = "questions";
function doPost(e) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  if (sh.getLastRow() === 0) sh.appendRow(["time","name","phone","location","floors","stage","question","source"]);
  const p = e.parameter || {};
  sh.appendRow([new Date(), p.name||"", p.phone||"", p.location||"", p.floors||"", p.stage||"", p.question||"", p.source||"website"]);
  // ঐচ্ছিক: নতুন প্রশ্নে ইমেইল
  try { MailApp.sendEmail("bosotbari.mm@gmail.com", "বসতবাড়ি: নতুন প্রশ্ন — " + (p.name||""), (p.phone||"") + "\n" + (p.location||"") + " · " + (p.floors||"") + " · " + (p.stage||"") + "\n\n" + (p.question||"")); } catch (err) {}
  return ContentService.createTextOutput(JSON.stringify({ok:true})).setMimeType(ContentService.MimeType.JSON);
}
function doGet() { return ContentService.createTextOutput("ok"); }
