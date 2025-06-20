from bs4 import BeautifulSoup
from patchright.async_api import async_playwright
import asyncio
import csv
from datetime import datetime
import json

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        try:
            # Set timeout yang lebih lama
            page.set_default_timeout(120000)  
            
            print("Membuka halaman...")
            # Buka halaman dengan timeout yang lebih lama
            await page.goto("https://www.alpinestars.com/collections/moto-apparel", 
                          wait_until='domcontentloaded',
                          timeout=60000)
            
            print("Menunggu halaman dimuat...")
            await asyncio.sleep(5)  # Tunggu sebentar untuk memastikan halaman dimuat
            
            # Tunggu dan klik tombol "Accept" jika muncul
            try:
                await page.wait_for_selector('button:has-text("Accept")', timeout=10000)
                await page.click('button:has-text("Accept")')
                print("Tombol Accept diklik.")
            except Exception:
                print("Tombol Accept tidak ditemukan atau sudah tidak muncul.")
            
            # Tunggu sampai elemen muncul dan pastikan halaman dimuat
            print("Menunggu elemen produk muncul...")
            
            # Ambil semua elemen produk menggunakan XPath
            product_cards = await page.query_selector_all('//*[@id="main-collection-product-grid"]/ol/li')
            
            # Buat nama file CSV dengan timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filename = f"alpinestars_products_{timestamp}.csv"
            
            # Tulis data ke CSV dan simpan juga ke list untuk JSON
            data_list = []
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Nama Produk', 'Warna', 'Harga', 'Kategori Produk'])

                for idx, card in enumerate(product_cards, start=1):
                    # Nama Produk
                    product_name_elem = await card.query_selector('xpath=.//div/div[2]/a/p')
                    product_name = await product_name_elem.inner_text() if product_name_elem else "N/A"

                    # Warna
                    color_elem = await card.query_selector('xpath=.//div/div[2]/div[2]')
                    color = await color_elem.inner_text() if color_elem else "N/A"

                    # Harga
                    price_elem = await card.query_selector('xpath=.//div/div[2]/div[3]/div/dl/div/dd')
                    price = await price_elem.inner_text() if price_elem else "N/A"

                    # Kategori Produk
                    category_elem = await card.query_selector('xpath=.//div/div[2]/div[2]/span[1]')
                    category = await category_elem.inner_text() if category_elem else "N/A"

                    writer.writerow([product_name, color, price, category])
                    data_list.append({
                        'Nama Produk': product_name,
                        'Warna': color,
                        'Harga': price,
                        'Kategori Produk': category
                    })
                    print(f"Nama: {product_name} | Warna: {color} | Harga: {price} | Kategori: {category}")
            
            # Simpan juga ke file JSON
            json_filename = f"alpinestars_products_{timestamp}.json"
            with open(json_filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data_list, jsonfile, ensure_ascii=False, indent=2)
            print(f"\nData juga berhasil disimpan ke file: {json_filename}")
            
            # Simpan struktur HTML utama untuk analisis
            main_grid = await page.query_selector('//*[@id="main-collection-product-grid"]')
            if main_grid:
                html_content = await main_grid.inner_html()
                with open('main_collection_product_grid.html', 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print('Struktur HTML produk utama disimpan ke main_collection_product_grid.html')
            
            # Tambah delay sebelum menutup browser
            print("Selesai mengambil data, menunggu sebelum menutup browser...")
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"Terjadi error: {str(e)}")
            # Tambah delay sebelum menutup browser jika terjadi error
            await asyncio.sleep(5)
        finally:
            print("Menutup browser...")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
