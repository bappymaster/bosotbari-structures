# ফর্ম → Google Sheet (৩ মিনিট, ফ্রি, bosotbari.mm@gmail.com দিয়ে লগইন করে)
1. sheets.new → নাম "বসতবাড়ি প্রশ্ন"।
2. Extensions → Apps Script → Code.gs-এর সব মুছে এই ফোল্ডারের Code.gs পেস্ট → Save।
3. Deploy → New deployment → Type: Web app → Execute as: Me → Who has access: Anyone → Deploy → Authorize।
4. যে URL আসবে (…/exec) সেটা website/ask.html-এ `const ENDPOINT = ""` এর ভিতরে বসান।
5. WhatsApp নম্বর ask.html-এ `wa.me/8801521479737` ঠিক আছে কি না দেখুন।
প্রতিটি প্রশ্ন শিটে জমা হবে এবং ইমেইলে যাবে। Facebook কমেন্ট/ইনবক্সের প্রশ্নও একই শিটে হাতে লিখে রাখুন (source = facebook)।
