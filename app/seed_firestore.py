import json
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-01-21daa4813152"
db = firestore.Client(project=PROJECT_ID)

PLATFORMS_DATA = [
    {
        "issue_id": "child-care",
        "issue_name": "Child Care",
        "parties": {
            "caq": {
                "party_name": "Coalition Avenir Québec",
                "leader": "François Legault",
                "color": "#51a5e1",
                "key_promises": [
                    "Turn school supplies supplement into a back-to-school supplement up to $250/child based on income.",
                    "Introduce new tax credit reimbursing up to 75% of school-day child-care fees (up to $1,309).",
                    "Convert 5,000 private child-care spots into subsidized ones and create 5,000 new subsidized spots.",
                    "Offer 2 additional weeks parental leave for fathers and up to 4 weeks paid leave for grandparents/relatives.",
                    "Increase Supplement for Handicapped Children by $50/month to $291/month."
                ]
            },
            "plq": {
                "party_name": "Quebec Liberal Party",
                "leader": "Marc Tanguay",
                "color": "#D71920",
                "key_promises": [
                    "Plans under development and to be announced ahead of election."
                ]
            },
            "qs": {
                "party_name": "Québec Solidaire",
                "leader": "Gabriel Nadeau-Dubois & Émilise Lessard-Therrien",
                "color": "#3c4349",
                "key_promises": [
                    "Implement a universal school food program across Quebec.",
                    "Replace school supplies payment with a government bulk purchasing and redistribution system for all parents."
                ]
            },
            "pq": {
                "party_name": "Parti Québécois",
                "leader": "Paul St-Pierre Plamondon",
                "color": "#134386",
                "key_promises": [
                    "Plans under development and to be announced ahead of election."
                ]
            },
            "pcq": {
                "party_name": "Conservative Party of Quebec",
                "leader": "Éric Duhaime",
                "color": "#0A1F54",
                "key_promises": [
                    "Maintain funding for public child-care network.",
                    "Enhance child-care expense tax credit for $950 annual savings for middle class.",
                    "Offer home child-care allowance of $100 per week."
                ]
            }
        }
    },
    {
        "issue_id": "cost-of-living",
        "issue_name": "Cost of Living",
        "parties": {
            "caq": {
                "party_name": "Coalition Avenir Québec",
                "leader": "François Legault",
                "color": "#51a5e1",
                "key_promises": [
                    "Invest $1,000 in RESP for every child born in Quebec starting fall 2027.",
                    "Raise seniors' assistance tax credit by $200 to $2,200 for low-income seniors aged 70+.",
                    "Shield up to $35,000 employment income from tax for seniors 65+ working essential jobs facing shortages."
                ]
            },
            "plq": {
                "party_name": "Quebec Liberal Party",
                "leader": "Marc Tanguay",
                "color": "#D71920",
                "key_promises": [
                    "Platform promises under development."
                ]
            },
            "qs": {
                "party_name": "Québec Solidaire",
                "leader": "Gabriel Nadeau-Dubois",
                "color": "#3c4349",
                "key_promises": [
                    "Increase minimum wage to $20/hour by May 1, 2027.",
                    "Create state-owned grocery stores to compete with food oligopolies and cap margins at 2%.",
                    "Counter shrinkflation, dynamic pricing, and hidden fees.",
                    "Abolish QST sales tax on used goods; make contraception & menstrual hygiene products free."
                ]
            },
            "pq": {
                "party_name": "Parti Québécois",
                "leader": "Paul St-Pierre Plamondon",
                "color": "#134386",
                "key_promises": [
                    "Ban surveillance pricing in grocery stores based on personal data.",
                    "Abolish Quebec sales tax (QST) on used goods."
                ]
            },
            "pcq": {
                "party_name": "Conservative Party of Quebec",
                "leader": "Éric Duhaime",
                "color": "#0A1F54",
                "key_promises": [
                    "Withdraw Quebec from cap-and-trade carbon market and suspend provincial gas tax for 5 months.",
                    "Raise basic personal income tax exemption to $35,242 (zero tax under $35,242).",
                    "Abolish QST sales tax on used goods."
                ]
            }
        }
    },
    {
        "issue_id": "economy-tariffs",
        "issue_name": "Economy & Tariffs",
        "parties": {
            "caq": {
                "party_name": "Coalition Avenir Québec",
                "leader": "François Legault",
                "color": "#51a5e1",
                "key_promises": [
                    "$13B increase in Quebec Infrastructure Plan (total $180B), 75% dedicated to maintenance.",
                    "Commitment to balance provincial budget by 2029-30."
                ]
            },
            "plq": {
                "party_name": "Quebec Liberal Party",
                "leader": "Marc Tanguay",
                "color": "#D71920",
                "key_promises": [
                    "Reduce exports to US by 15% through trade alliances in Canada, Europe, and Francophonie.",
                    "Gradually reduce SME corporate tax rate from 11.5% to 10%.",
                    "Convert 25% of SME assistance into non-repayable direct funding.",
                    "Apply 15% local preference margin across all government public calls for tender."
                ]
            },
            "qs": {
                "party_name": "Québec Solidaire",
                "leader": "Gabriel Nadeau-Dubois",
                "color": "#3c4349",
                "key_promises": [
                    "Tax on fortunes starting at $25M (recovering $5B).",
                    "Create a 'Trump provision' fund up to $1B/year to address US tariff threats.",
                    "Cap executive salaries for companies receiving public subsidies."
                ]
            },
            "pq": {
                "party_name": "Parti Québécois",
                "leader": "Paul St-Pierre Plamondon",
                "color": "#134386",
                "key_promises": [
                    "Lower corporate income taxes from 11.5% to 9.5% by abolishing Fonds de développement économique.",
                    "Shrink public sector payroll costs by 2.5% over 3 years via attrition and efficiency.",
                    "Create Secretariat for Government Efficiency and Regulatory Relief."
                ]
            },
            "pcq": {
                "party_name": "Conservative Party of Quebec",
                "leader": "Éric Duhaime",
                "color": "#0A1F54",
                "key_promises": [
                    "Gradually reduce corporate tax rate from 11.5% to 4.7%.",
                    "Exploit Utica shale gas generating $9.4B in royalties over 10 years.",
                    "Reduce red tape for Quebec companies by 30%."
                ]
            }
        }
    },
    {
        "issue_id": "education",
        "issue_name": "Education",
        "parties": {
            "caq": {
                "party_name": "Coalition Avenir Québec",
                "leader": "François Legault",
                "color": "#51a5e1",
                "key_promises": [
                    "Focus on current school infrastructure modernization without holding an education convention."
                ]
            },
            "plq": {
                "party_name": "Quebec Liberal Party",
                "leader": "Marc Tanguay",
                "color": "#D71920",
                "key_promises": [
                    "Hold a general convention on education in Quebec.",
                    "Remove provisions in Charter of French Language reducing English college spots (maintain 85% French / 15% English CEGEP ratio).",
                    "Add 1,000 specialized professional resources to public schools starting 2027-28."
                ]
            },
            "qs": {
                "party_name": "Québec Solidaire",
                "leader": "Gabriel Nadeau-Dubois",
                "color": "#3c4349",
                "key_promises": [
                    "Hold general education convention and establish a common education network uniting public/private schools.",
                    "Hire 1,500 support staff and 500 professionals to cut dropout rates by 50%.",
                    "$135M to support students with disabilities and funding paid internships for new teachers."
                ]
            },
            "pq": {
                "party_name": "Parti Québécois",
                "leader": "Paul St-Pierre Plamondon",
                "color": "#134386",
                "key_promises": [
                    "Hold general education convention within first 100 days.",
                    "Extend Charter of French Language (Bill 101) to CEGEPs.",
                    "Allocate 10% of grade for all assignments to quality of French language.",
                    "Require 60 minutes of physical education daily in elementary and high schools."
                ]
            },
            "pcq": {
                "party_name": "Conservative Party of Quebec",
                "leader": "Éric Duhaime",
                "color": "#0A1F54",
                "key_promises": [
                    "Increase physical education periods in schools and add 4th gym course in CEGEP.",
                    "Introduce annual standardized physical fitness tests in schools."
                ]
            }
        }
    },
    {
        "issue_id": "environment-natural-resources",
        "issue_name": "Environment & Natural Resources",
        "parties": {
            "caq": {
                "party_name": "Coalition Avenir Québec",
                "leader": "François Legault",
                "color": "#51a5e1",
                "key_promises": [
                    "Double share of natural resource royalty revenues allocated to regions ($38M to $76M annually).",
                    "Finalize Churchill Falls agreement with NFLD securing 10,000 MW clean electricity alongside $45B Hydro-Québec investments."
                ]
            },
            "plq": {
                "party_name": "Quebec Liberal Party",
                "leader": "Marc Tanguay",
                "color": "#D71920",
                "key_promises": [
                    "Create Mining Community Development Fund granting regional county municipalities control over local projects."
                ]
            },
            "qs": {
                "party_name": "Québec Solidaire",
                "leader": "Gabriel Nadeau-Dubois",
                "color": "#3c4349",
                "key_promises": [
                    "Block all oil and gas pipeline projects on Quebec territory; oppose shale gas.",
                    "Commit to 37.5% greenhouse gas emission cuts below 1990 levels by 2030 and carbon neutrality by 2050."
                ]
            },
            "pq": {
                "party_name": "Parti Québécois",
                "leader": "Paul St-Pierre Plamondon",
                "color": "#134386",
                "key_promises": [
                    "Allocate 10% of mining royalties directly to regions.",
                    "Policy prioritizing local wood procurement in public projects.",
                    "Call for permanent suspension of federal gas excise tax."
                ]
            },
            "pcq": {
                "party_name": "Conservative Party of Quebec",
                "leader": "Éric Duhaime",
                "color": "#0A1F54",
                "key_promises": [
                    "Withdraw Quebec from cap-and-trade carbon market and eliminate Electrification and Climate Change Fund.",
                    "Exploit Utica shale gas generating $9.4B over 10 years.",
                    "Delegate timber volume management to local regions."
                ]
            }
        }
    },
    {
        "issue_id": "health-care",
        "issue_name": "Health Care",
        "parties": {
            "caq": {
                "party_name": "Coalition Avenir Québec",
                "leader": "François Legault",
                "color": "#51a5e1",
                "key_promises": [
                    "Invest extra $1B over 4 years in home care.",
                    "Redirect surgeries to public network after 6 months and private sector after 9 months.",
                    "Use private clinics for 100,000 extra imaging exams (MRIs, CT scans) covered by Medicare (RAMQ).",
                    "Open discussions on mixed public-private medical practice."
                ]
            },
            "plq": {
                "party_name": "Quebec Liberal Party",
                "leader": "Marc Tanguay",
                "color": "#D71920",
                "key_promises": [
                    "Temporary contribution holiday from Health Services Fund for SMEs.",
                    "Expand access to primary care physicians and modernize healthcare delivery."
                ]
            },
            "qs": {
                "party_name": "Québec Solidaire",
                "leader": "Gabriel Nadeau-Dubois",
                "color": "#3c4349",
                "key_promises": [
                    "Strengthen public healthcare network and phase out reliance on private healthcare agencies.",
                    "Expand public dental and mental health coverage under RAMQ."
                ]
            },
            "pq": {
                "party_name": "Parti Québécois",
                "leader": "Paul St-Pierre Plamondon",
                "color": "#134386",
                "key_promises": [
                    "Focus healthcare funding directly on frontline staff and regional clinics.",
                    "Streamline healthcare administration and reduce bureaucratic overhead."
                ]
            },
            "pcq": {
                "party_name": "Conservative Party of Quebec",
                "leader": "Éric Duhaime",
                "color": "#0A1F54",
                "key_promises": [
                    "Offer mixed medical practice and entrust management of some hospitals to private companies.",
                    "Ensure free care at private clinics when public network delays are unreasonable."
                ]
            }
        }
    }
]

def seed():
    print(f"Seeding Firestore collection 'quebec_2026_platforms' on project {PROJECT_ID}...")
    col_ref = db.collection("quebec_2026_platforms")
    for doc in PLATFORMS_DATA:
        issue_id = doc["issue_id"]
        col_ref.document(issue_id).set(doc)
        print(f"  ✓ Seeded issue: {doc['issue_name']} ({issue_id})")
    print("Seeding complete successfully!")

if __name__ == "__main__":
    seed()
