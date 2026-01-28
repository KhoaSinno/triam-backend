import asyncio
from app.services.pdf_service import extract_chapters_smart, extract_text_from_pdf

async def test_pdf_extraction():
    """Test PDF extraction with the bi_mat_cua_mot_tri_nho.pdf file"""
    print("=" * 60)
    print("TEST: PDF Extraction")
    print("=" * 60)
    
    # Test 1: extract_text_from_pdf (simple text extraction)
    print("\n[TEST 1] Testing extract_text_from_pdf (2 pages)...")
    with open("uploads/bi_mat_cua_mot_tri_nho.pdf", "rb") as f:
        text = await extract_text_from_pdf(f, max_pages=2)
        print(f"✓ Extracted {len(text)} characters")
        print(f"Preview: {text[:200]}...")
    
    # Test 2: extract_chapters_smart (3-level smart extraction)
    print("\n[TEST 2] Testing extract_chapters_smart...")
    with open("uploads/bi_mat_cua_mot_tri_nho.pdf", "rb") as f:
        chapters = await extract_chapters_smart(f, pages_per_chunk=5)
        print(f"✓ Found {len(chapters)} chapters/sections")
        
        for i, ch in enumerate(chapters[:5], 1):
            print(f"\n  Chapter {i}:")
            print(f"    Title: {ch['title']}")
            print(f"    Page: {ch['page_start']}")
            print(f"    Text length: {len(ch['text'])} chars")
            print(f"    Preview: {ch['text'][:100]}...")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_pdf_extraction())
