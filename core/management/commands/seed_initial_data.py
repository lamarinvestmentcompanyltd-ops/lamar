import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from core.models import Material, Partner, TeamMember, Testimonial, WorkPhoto, WorkPhotoCategory

SEED_DIR = os.path.join(settings.BASE_DIR, "core", "seed_data")

TEAM = [
    {"name": 'Mupenda Aimable', "role": 'Directing Manager', "file": 'team/mupenda_aimable.jpeg', "order": 1},
    {"name": 'Murenzi Charles', "role": 'Software Engineer', "file": 'team/murenzi_charles.jpeg', "order": 2},
    {"name": 'Pascal', "role": 'Cleaning Team Lead', "file": 'team/pascal.jpeg', "order": 3},
    {"name": 'uwase Naomi', "role": 'Operational Manager', "file": 'team/uwase_naomi.jpeg', "order": 4},
]

PARTNERS = [
    {"name": 'East African Christian College(EACC)', "file": 'partners/east_african_christian_college_eacc.png', "website": 'https://www.eacc.ac.rw/eacc', "order": 1},
    {"name": 'Ecole Sainte Anne de Kigali', "file": 'partners/ecole_sainte_anne_de_kigali.png', "website": 'https://ecolesainteanne.org/', "order": 2},
    {"name": 'Ruhengeri Referral Hospital', "file": 'partners/ruhengeri_referral_hospital.png', "website": 'https://www.rrh.gov.rw/', "order": 3},
    {"name": 'RSSB', "file": 'partners/rssb.png', "website": 'https://www.rssb.rw/', "order": 4},
    {"name": 'Covenant Plaza', "file": 'partners/covenant_plaza.jpeg', "website": '', "order": 4},
]

TESTIMONIALS = [
    {
        "client_name": "Jean Paul K.",
        "client_detail": "Office Manager, Kigali",
        "quote": "Lamar has kept our office spotless for over a year. They're reliable, thorough, and easy to work with.",
        "rating": 5,
        "order": 1,
    },
    {
        "client_name": "Aline Uwase",
        "client_detail": "Homeowner, Kicukiro",
        "quote": "We booked a one-time deep clean before moving in and it made all the difference. Highly recommend.",
        "rating": 5,
        "order": 2,
    },
    {
        "client_name": "Diane M.",
        "client_detail": "Facility Coordinator",
        "quote": "Our school's cleaning schedule runs smoothly thanks to Lamar's consistency and attention to health and safety.",
        "rating": 5,
        "order": 3,
    },
]

WORK_PHOTOS = [
    {"file": "work/cleaning-table.jpg", "caption": "Careful surface cleaning", "category": WorkPhotoCategory.GENERAL, "pair_key": "", "order": 1},
    {"file": "work/cleaning-vacuum.jpg", "caption": "Vacuuming a living space", "category": WorkPhotoCategory.GENERAL, "pair_key": "", "order": 2},
    {"file": "work/cleaning-wall.jpg", "caption": "Detailed wall and skirting-board cleaning", "category": WorkPhotoCategory.GENERAL, "pair_key": "", "order": 3},
]

# Product photos the client provided, seeded alongside the matching item.
# Anything without a "file" key still seeds fine — it just renders with the
# neutral placeholder tile on the Our Materials page until a photo is added.
MATERIALS = [
    {"name": "Industrial Vacuum Cleaner", "category": "equipment",
     "description": "High-suction commercial vacuums for carpets and hard floors.",
     "file": "materials/industrial-vacuum-cleaner.png", "order": 1},
    {"name": "Floor Buffer / Polisher", "category": "equipment",
     "description": "Used for polishing and maintaining hard floor surfaces.",
     "file": "materials/floor-buffer-polisher.png", "order": 2},
    {"name": "Pressure Washer", "category": "equipment",
     "description": "For exterior surfaces, walkways, and post-construction cleanup.",
     "file": "materials/pressure-washer.png", "order": 3},
    {"name": "Wet & Dry Mop System", "category": "equipment",
     "description": "Colour-coded mopping system to prevent cross-contamination between areas.",
     "file": "materials/wet-dry-mop-system.png", "order": 4},

    {"name": "Multi-Surface Disinfectant", "category": "chemicals",
     "description": "Hospital-grade disinfectant safe on most hard surfaces.",
     "file": "materials/multi-surface-disinfectant.png", "order": 1},
    {"name": "Glass & Window Cleaner", "category": "chemicals",
     "description": "Streak-free formula for windows, mirrors, and glass partitions.",
     "file": "materials/glass-window-cleaner.png", "order": 2},
    {"name": "Carpet & Upholstery Shampoo", "category": "chemicals",
     "description": "Deep-cleaning shampoo for carpets, rugs, and fabric furniture.",
     "file": "materials/carpet-upholstery-shampoo.png", "order": 3},
    {"name": "Floor Degreaser", "category": "chemicals",
     "description": "Heavy-duty degreaser for kitchens and industrial floors.",
     "file": "materials/floor-degreaser.png", "order": 4},

    {"name": "Microfiber Cloths", "category": "consumables",
     "description": "Colour-coded per area to prevent cross-contamination.",
     "file": "materials/microfiber-cloths.png", "order": 1},
    {"name": "Trash Liners & Bin Bags", "category": "consumables",
     "description": "Various sizes for offices, washrooms, and outdoor bins.",
     "file": "materials/trash-liners-bin-bags.png", "order": 2},
    {"name": "Paper Towels & Tissue Refills", "category": "consumables",
     "description": "Restocked as part of ongoing commercial contracts.",
     "file": "materials/paper-towels-tissue-refills.png", "order": 3},

    {"name": "Nitrile Gloves", "category": "safety",
     "description": "Worn during all chemical handling and washroom sanitation tasks.",
     "file": "materials/nitrile-gloves.png", "order": 1},
    {"name": "Safety Goggles", "category": "safety",
     "description": "Used when handling concentrated chemicals or during pressure washing.",
     "file": "materials/safety-goggles.png", "order": 2},
    {"name": "Wet Floor Signage", "category": "safety",
     "description": "Placed during and after mopping to protect staff and building occupants.",
     "file": "materials/wet-floor-signage.png", "order": 3},
    {"name": "Respirator Masks", "category": "safety",
     "description": "Used for post-construction cleanup and dust-heavy environments.",
     "file": "materials/respirator-masks.png", "order": 4},
]


class Command(BaseCommand):
    help = "Seed initial team, partners, testimonials, and gallery photos (safe to re-run — skips ones that already exist)."

    def handle(self, *args, **options):
        for entry in TEAM:
            if TeamMember.objects.filter(name=entry["name"]).exists():
                self.stdout.write(f"Skipping (exists): {entry['name']}")
                continue
            path = os.path.join(SEED_DIR, entry["file"])
            member = TeamMember(name=entry["name"], role=entry["role"], order=entry["order"])
            with open(path, "rb") as f:
                member.photo.save(os.path.basename(path), File(f), save=True)
            self.stdout.write(self.style.SUCCESS(f"Added team member: {entry['name']}"))

        for entry in PARTNERS:
            if Partner.objects.filter(name=entry["name"]).exists():
                self.stdout.write(f"Skipping (exists): {entry['name']}")
                continue
            path = os.path.join(SEED_DIR, entry["file"])
            partner = Partner(name=entry["name"], website=entry.get("website", ""), order=entry["order"])
            with open(path, "rb") as f:
                partner.logo.save(os.path.basename(path), File(f), save=True)
            self.stdout.write(self.style.SUCCESS(f"Added partner: {entry['name']}"))

        for entry in TESTIMONIALS:
            if Testimonial.objects.filter(client_name=entry["client_name"]).exists():
                self.stdout.write(f"Skipping (exists): {entry['client_name']}")
                continue
            Testimonial.objects.create(
                client_name=entry["client_name"],
                client_detail=entry["client_detail"],
                quote=entry["quote"],
                rating=entry["rating"],
                order=entry["order"],
            )
            self.stdout.write(self.style.SUCCESS(f"Added testimonial: {entry['client_name']}"))

        for entry in WORK_PHOTOS:
            if WorkPhoto.objects.filter(caption=entry["caption"], category=entry["category"]).exists():
                self.stdout.write(f"Skipping (exists): {entry['file']}")
                continue
            path = os.path.join(SEED_DIR, entry["file"])
            photo = WorkPhoto(
                caption=entry["caption"],
                category=entry["category"],
                pair_key=entry["pair_key"],
                order=entry["order"],
            )
            with open(path, "rb") as f:
                photo.image.save(os.path.basename(path), File(f), save=True)
            self.stdout.write(self.style.SUCCESS(f"Added work photo: {entry['file']}"))

        for entry in MATERIALS:
            if Material.objects.filter(name=entry["name"]).exists():
                self.stdout.write(f"Skipping (exists): {entry['name']}")
                continue
            material = Material(
                name=entry["name"],
                category=entry["category"],
                description=entry["description"],
                order=entry["order"],
            )
            if entry.get("file"):
                path = os.path.join(SEED_DIR, entry["file"])
                with open(path, "rb") as f:
                    material.image.save(os.path.basename(path), File(f), save=False)
            material.save()
            self.stdout.write(self.style.SUCCESS(f"Added material: {entry['name']}"))

        self.stdout.write(self.style.SUCCESS(
            "Done. Visit /, /about/, /gallery/, and /materials/ to see everything. "
            "Sample testimonials, gallery photos, and materials are placeholders — "
            "replace them from /admin/ with real content whenever you're ready."
        ))
