from flask import Flask, render_template, request, redirect, url_for, session
import time

app = Flask(__name__)
app.secret_key = "yazn_project"

questions = [
    ("الشبكة هي ربط جهازين أو أكثر لتبادل البيانات", True),
    ("الشبكة المحلية LAN تغطي مساحة جغرافية صغيرة", True),
    ("الشبكة الواسعة WAN تستخدم داخل المباني فقط", False),
    ("الإنترنت مثال على شبكة WAN", True),
    ("الشبكة السلكية تعتمد على الكابلات", True),
    ("WLAN هي شبكة لاسلكية", True),
    ("MAN تغطي مدينة كاملة", True),
    ("PAN أكبر من LAN", False),
    ("Bluetooth مثال على شبكة PAN", True),
    ("WAN أسرع دائمًا من LAN", False),
    ("الراوتر يستخدم لربط شبكتين مختلفتين", True),
    ("السويتش يعمل في الطبقة الثانية من نموذج OSI", True),
    ("الهَب أكثر كفاءة من السويتش", False),
    ("المودم يستخدم للاتصال بالإنترنت", True),
    ("Access Point يستخدم للشبكات اللاسلكية", True),
    ("TCP بروتوكول موثوق", True),
    ("UDP بروتوكول غير موثوق", True),
    ("HTTP بروتوكول آمن", False),
    ("HTTPS يستخدم التشفير", True),
    ("FTP يستخدم لنقل الملفات", True),
    ("عنوان IP يحدد هوية الجهاز على الشبكة", True),
    ("IPv4 يتكون من 32 بت", True),
    ("IPv6 أقصر من IPv4", False),
    ("عنوان IP يمكن تكراره في نفس الشبكة", False),
    ("192.168.1.1 عنوان IP خاص", True),
    ("DNS يحول اسم الموقع إلى عنوان IP", True),
    ("DHCP يوزع عناوين IP تلقائيًا", True),
    ("DNS يستخدم لتشفير البيانات", False),
    ("بدون DNS لا يمكن استخدام IP", False),
    ("DHCP يقلل الأخطاء الناتجة عن التوزيع اليدوي", True),
    ("نموذج OSI يتكون من 7 طبقات", True),
    ("الطبقة الفيزيائية مسؤولة عن الكابلات والإشارات", True),
    ("طبقة النقل هي الطبقة السابعة", False),
    ("TCP يعمل في طبقة النقل", True),
    ("HTTP يعمل في طبقة التطبيق", True),
    ("الجدار الناري Firewall يحمي الشبكة من الهجمات", True),
    ("التشفير يمنع قراءة البيانات من غير المصرح لهم", True),
    ("الفيروسات لا تؤثر على الشبكات", False),
    ("VPN يوفر اتصالًا آمنًا عبر الإنترنت", True),
    ("كلمة المرور القوية غير مهمة", False),
    ("Bandwidth تعني عرض النطاق الترددي", True),
    ("Latency تعني زمن التأخير في الشبكة", True),
    ("Ping يستخدم لاختبار الاتصال بين جهازين", True),
    ("MAC Address يمكن تغييره دائمًا", False),
    ("كل جهاز شبكة يمتلك MAC Address فريد", True),
    ("السيرفر يقدم خدمات للأجهزة الأخرى", True),
    ("العميل Client لا يطلب خدمات من السيرفر", False),
    ("الشبكات تسهل مشاركة الموارد", True),
    ("بدون شبكة لا يمكن الاتصال بالإنترنت", True),
    ("تقنية الشبكات غير مهمة في العصر الحديث", False),
]

@app.route("/")
def home():
    session.clear()
    session["answers"] = []
    session["score"] = 0
    session["start_time"] = time.time()
    return render_template("home.html")

@app.route("/question/<int:num>", methods=["GET", "POST"])
def question(num):
    if num > len(questions):
        return redirect(url_for("result"))

    if request.method == "POST":
        user_answer = request.form.get("answer") == "true"
        correct = questions[num-1][1]

        session["answers"].append({
            "question": questions[num-1][0],
            "user": user_answer,
            "correct": correct
        })

        if user_answer == correct:
            session["score"] += 1

        return redirect(url_for("question", num=num+1))

    elapsed = int(time.time() - session["start_time"])
    remaining = max(0, 1800 - elapsed)

    if remaining <= 0:
        return redirect(url_for("result"))

    return render_template(
        "question.html",
        number=num,
        question=questions[num-1][0],
        total=len(questions),
        remaining=remaining
    )

@app.route("/result")
def result():
    return render_template(
        "result.html",
        score=session["score"],
        total=len(questions)
    )

@app.route("/print")
def print_result():
    return render_template(
        "print.html",
        answers=session["answers"],
        score=session["score"],
        total=len(questions)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)