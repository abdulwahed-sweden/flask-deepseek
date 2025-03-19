from flask import Flask, render_template, jsonify
import pandas as pd
import random

app = Flask(__name__)

# تحميل بيانات المدن الحقيقية
def load_city_data():
    """ تحميل بيانات المدن من ملف CSV """
    file_path = "data/worldcities.csv"  # تأكد من أن المسار صحيح
    
    try:
        df = pd.read_csv(file_path)
        # التحقق من وجود الأعمدة المطلوبة
        required_columns = {"city", "country", "lat", "lng", "admin_name", "population"}
        if not required_columns.issubset(df.columns):
            raise ValueError("ملف CSV لا يحتوي على الأعمدة المطلوبة.")

        # تصفية المدن متوسطة الحجم فقط (بين 100 ألف و 2 مليون نسمة)
        df = df[(df["population"] > 100000) & (df["population"] < 2000000)]
        return df
    except Exception as e:
        print(f"⚠️ خطأ في تحميل البيانات: {e}")
        return pd.DataFrame()

cities_df = load_city_data()

# دالة لاختيار مدينة عشوائية غير مشهورة
def get_random_city():
    """ إرجاع مدينة عشوائية حقيقية ولكن غير معروفة عالميًا """
    if cities_df.empty:
        return None

    city_data = cities_df.sample(n=1).iloc[0]
    return {
        "city": city_data["city"],
        "country": city_data["country"],
        "lat": city_data["lat"],
        "lng": city_data["lng"],
        "admin_name": city_data["admin_name"],
        "population": int(city_data["population"])
    }

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/random_city', methods=['GET'])
def random_city():
    city_info = get_random_city()
    if city_info:
        return jsonify(city_info)
    return jsonify({"error": "لم يتم العثور على بيانات مدينة صالحة!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
