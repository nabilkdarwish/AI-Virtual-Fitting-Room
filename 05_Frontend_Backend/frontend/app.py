"""Streamlit interface for the AI Virtual Fitting Room."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CATALOG_FILE = PROJECT_ROOT / "Dataset" / "Catalog" / "catalog_metadata.json"
PAGE_SIZE = 18


@st.cache_data(show_spinner=False)
def load_catalog() -> list[dict[str, Any]]:
    """Load catalog metadata from the repository's shared dataset."""
    try:
        with CATALOG_FILE.open(encoding="utf-8") as catalog_file:
            data = json.load(catalog_file)
    except (OSError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def image_for(item: dict[str, Any]) -> Path | None:
    """Return a catalog image path only when it stays inside this repository."""
    relative_path = item.get("image_path")
    if not relative_path:
        return None

    image_path = (PROJECT_ROOT / str(relative_path)).resolve()
    try:
        image_path.relative_to(PROJECT_ROOT)
    except ValueError:
        return None
    return image_path if image_path.is_file() else None


def display_name(item: dict[str, Any]) -> str:
    return str(item.get("product_name") or item.get("product_id") or "Garment")


def show_garment_image(item: dict[str, Any], *, width: str = "stretch") -> None:
    path = image_for(item)
    if path:
        st.image(str(path), use_container_width=(width == "stretch"))
    else:
        st.caption("صورة المنتج غير موجودة في مجلد Dataset/Catalog.")


st.set_page_config(
    page_title="غرفة القياس الافتراضية",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded",
)

catalog = load_catalog()
if not catalog:
    st.error("تعذر تحميل الكتالوج. تأكد من وجود Dataset/Catalog/catalog_metadata.json.")
    st.stop()

catalog_by_id = {str(item.get("product_id")): item for item in catalog}
st.session_state.setdefault("selected_product_id", "")
st.session_state.setdefault("confirmed_product_id", "")
st.session_state.setdefault("catalog_page", 0)

st.title("🪞 غرفة القياس الافتراضية")
st.caption("التقط صورة أو ارفعها، ثم اختر قطعة من كتالوج الملابس.")

with st.sidebar:
    st.header("تصفية الكتالوج")
    categories = sorted(
        {str(item.get("target_category", "Other")) for item in catalog}
    )
    selected_category = st.selectbox("الفئة", ["الكل", *categories])
    category_items = catalog if selected_category == "الكل" else [
        item for item in catalog if item.get("target_category") == selected_category
    ]

    clothing_types = sorted(
        {str(item.get("clothing_type", "Other")) for item in category_items}
    )
    selected_type = st.selectbox("نوع الملابس", ["الكل", *clothing_types])

    colors = sorted(
        {str(item.get("color", "Other")) for item in category_items}
    )
    selected_color = st.selectbox("اللون", ["كل الألوان", *colors])
    search_text = st.text_input("بحث بالاسم أو رقم المنتج")

    st.divider()
    st.subheader("القطعة المختارة")
    selected_item = catalog_by_id.get(st.session_state.selected_product_id)
    if selected_item:
        show_garment_image(selected_item)
        st.write(display_name(selected_item))
        st.caption(f"رقم المنتج: {selected_item.get('product_id', '—')}")
        if st.button("إلغاء الاختيار", use_container_width=True):
            st.session_state.selected_product_id = ""
            st.session_state.confirmed_product_id = ""
            st.rerun()
    else:
        st.caption("اختر قطعة من الكتالوج لعرضها هنا.")

left, right = st.columns([1, 1.25], gap="large")
with left:
    st.subheader("صورة المستخدم")
    image_source = st.radio(
        "مصدر الصورة",
        ["التقاط بالكاميرا", "رفع صورة"],
        horizontal=True,
        label_visibility="collapsed",
    )
    if image_source == "التقاط بالكاميرا":
        person_image = st.camera_input("التقط صورة")
    else:
        person_image = st.file_uploader(
            "اختر صورة بصيغة JPG أو PNG",
            type=["jpg", "jpeg", "png"],
        )

    if person_image:
        st.image(person_image, caption="الصورة التي سيتم استخدامها", use_container_width=True)
    else:
        st.info("التقط صورة أو ارفع صورة لعرضها هنا.")

with right:
    st.subheader("معاينة الاختيار")
    if selected_item:
        preview_columns = st.columns(2)
        with preview_columns[0]:
            if person_image:
                st.image(person_image, caption="صورة المستخدم", use_container_width=True)
            else:
                st.info("صورة المستخدم غير محددة")
        with preview_columns[1]:
            show_garment_image(selected_item)
            st.caption(display_name(selected_item))

        if st.button("تأكيد اختيار القطعة", type="primary", use_container_width=True):
            st.session_state.confirmed_product_id = str(selected_item.get("product_id", ""))
        if st.session_state.confirmed_product_id == str(selected_item.get("product_id", "")):
            st.success(f"تم حفظ اختيار المنتج رقم {selected_item.get('product_id')}.")
        st.caption(
            "هذه معاينة للصورة والقطعة المختارة. توليد صورة القياس يحتاج إلى ربط نموذج Virtual Try-On."
        )
    else:
        st.info("اختر قطعة من الكتالوج لعرضها بجانب صورتك.")

st.divider()
st.subheader("كتالوج الملابس")

filtered_items = []
normalized_search = search_text.strip().casefold()
for item in category_items:
    if selected_type != "الكل" and item.get("clothing_type") != selected_type:
        continue
    if selected_color != "كل الألوان" and item.get("color") != selected_color:
        continue
    searchable_text = f"{display_name(item)} {item.get('product_id', '')}".casefold()
    if normalized_search and normalized_search not in searchable_text:
        continue
    filtered_items.append(item)

if not filtered_items:
    st.warning("لا توجد منتجات مطابقة للفلاتر الحالية.")
else:
    total_pages = max(1, (len(filtered_items) + PAGE_SIZE - 1) // PAGE_SIZE)
    st.session_state.catalog_page = min(st.session_state.catalog_page, total_pages - 1)
    page_columns = st.columns([1, 3, 1])
    with page_columns[0]:
        if st.button("← السابق", disabled=st.session_state.catalog_page == 0):
            st.session_state.catalog_page -= 1
            st.rerun()
    with page_columns[1]:
        st.caption(
            f"صفحة {st.session_state.catalog_page + 1} من {total_pages} · "
            f"{len(filtered_items)} منتج"
        )
    with page_columns[2]:
        if st.button("التالي →", disabled=st.session_state.catalog_page >= total_pages - 1):
            st.session_state.catalog_page += 1
            st.rerun()

    start = st.session_state.catalog_page * PAGE_SIZE
    visible_items = filtered_items[start : start + PAGE_SIZE]
    for row_start in range(0, len(visible_items), 3):
        cards = st.columns(3, gap="medium")
        for card, item in zip(cards, visible_items[row_start : row_start + 3]):
            product_id = str(item.get("product_id", ""))
            with card:
                show_garment_image(item)
                st.markdown(f"**{display_name(item)}**")
                st.caption(
                    f"{item.get('target_category', '—')} · "
                    f"{item.get('color', '—')} · #{product_id}"
                )
                is_selected = product_id == st.session_state.selected_product_id
                if st.button(
                    "تم الاختيار ✓" if is_selected else "اختيار القطعة",
                    key=f"select-{product_id}",
                    type="primary" if is_selected else "secondary",
                    use_container_width=True,
                ):
                    st.session_state.selected_product_id = product_id
                    st.session_state.confirmed_product_id = ""
                    st.rerun()
