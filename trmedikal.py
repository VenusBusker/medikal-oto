import feedparser
import json
import os
from datetime import datetime

# TÜRKÇE KAYNAKLAR (Medikal ve Genel Sağlık)
RSS_SOURCES = [
    "https://www.medimagazin.com.tr/rss",             # Medimagazin (Doktorlar için)
    "https://www.saglikaktuel.com/rss",               # Sağlık Aktüel
    "https://www.trthaber.com/saglik_articles.rss",    # TRT Haber Sağlık
    "https://www.cnnturk.com/feed/rss/saglik/haber"    # CNN Türk Sağlık
]

def haber_topla():
    yeni_haberler = []
    
    for url in RSS_SOURCES:
        try:
            feed = feedparser.parse(url)
            kaynak_adi = feed.feed.title if hasattr(feed.feed, 'title') else "MED_TR"
            
            for entry in feed.entries:
                haber = {
                    "title": f"{entry.title} - {kaynak_adi}",
                    "link": entry.link,
                    "pubDate": entry.published if hasattr(entry, 'published') else datetime.now().isoformat()
                }
                yeni_haberler.append(haber)
        except Exception as e:
            print(f"Hata: {url} taranamadı. {e}")

    # Tarihe göre sırala (En yeni en üstte)
    yeni_haberler.sort(key=lambda x: x['pubDate'], reverse=True)
    
    # JSON dosyasına kaydet
    with open("haberler_tr.json", "w", encoding="utf-8") as f:
        json.dump({"items": yeni_haberler[:100]}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    haber_topla()
