# LinkedIn Bot - Bağımsız Agent

Bu proje, LinkedIn'de otomatik paylaşım yapmak için tasarlanmış bağımsız bir AI agent'ıdır.

## Özellikler
- LinkedIn API ile OAuth 2.0 entegrasyonu
- Otomatik metin paylaşımı
- Token yönetimi

## Kurulum

```bash
# Repo'yu klonla
git clone <repo-url>
cd linkedin-bot

# Python sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

## Kullanım

```bash
# Paylaşım yap
python linkedin_bot.py --token "TOKEN" --person-urn "urn:li:person:xxx" --message "Merhaba Dünya!"
```

## Ortam Değişkenleri
- `LINKEDIN_TOKEN` - LinkedIn API access token
- `LINKEDIN_PERSON_URN` - Kullanıcının LinkedIn URN'si
