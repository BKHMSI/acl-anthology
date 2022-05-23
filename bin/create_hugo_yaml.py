#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019 Marcel Bollmann <marcel@bollmann.me>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Usage: create_hugo_yaml.py [--importdir=DIR] [--exportdir=DIR] [-c] [--debug] [--dry-run]

Creates YAML files containing all necessary Anthology data for the static website generator.

Options:
  --importdir=DIR          Directory to import XML files from. [default: {scriptdir}/../data/]
  --exportdir=DIR          Directory to write YAML files to.   [default: {scriptdir}/../build/data/]
  --debug                  Output debug-level log messages.
  -c, --clean              Delete existing files in target directory before generation.
  -n, --dry-run            Do not write YAML files (useful for debugging).
  -h, --help               Display this helpful text.
"""

from docopt import docopt
from collections import defaultdict
from tqdm import tqdm
import logging as log
import os
import yaml, yamlfix
import sys

try:
    from yaml import CSafeDumper as Dumper
except ImportError:
    from yaml import SafeDumper as Dumper

from anthology import Anthology
from anthology.utils import SeverityTracker, deconstruct_anthology_id, is_newstyle_id
from create_hugo_pages import check_directory


def export_anthology(anthology, outdir, clean=False, dryrun=False):
    # Prepare paper index
    papers = defaultdict(dict)
    citation_styles = {
        "acl": "association-for-computational-linguistics",
        # "apa": "apa-6th-edition",
        # "mla": "modern-language-association-7th-edition",
    }
    for id_, paper in anthology.papers.items():
        log.debug("export_anthology: processing paper '{}'".format(id_))
        data = paper.as_dict()
        data["title_html"] = paper.get_title("html")
        if "xml_title" in data:
            del data["xml_title"]
        # if 'title_ar' in data:
        #     data['title_af_html'], data['title_sq_html'], data['title_am_html'], data['title_ar_html'], data['title_hy_html'], data['title_az_html'], data['title_bn_html'], data['title_bs_html'], data['title_bg_html'], data['title_ca_html'], data['title_zh_html'], data['title_hr_html'], data['title_cs_html'], data['title_da_html'], data['title_nl_html'], data['title_et_html'], data['title_fl_html'], data['title_fi_html'], data['title_fr_html'], data['title_ka_html'], data['title_de_html'], data['title_el_html'], data['title_ha_html'], data['title_he_html'], data['title_hi_html'], data['title_hu_html'], data['title_is_html'], data['title_id_html'], data['title_ga_html'], data['title_it_html'], data['title_ja_html'], data['title_jv_html'], data['title_kk_html'], data['title_ko_html'], data['title_lt_html'], data['title_mk_html'], data['title_ms_html'], data['title_ml_html'], data['title_mt_html'], data['title_mn_html'], data['title_no_html'], data['title_fa_html'], data['title_pl_html'], data['title_pt_html'], data['title_ro_html'], data['title_ru_html'], data['title_sr_html'], data['title_si_html'], data['title_sk_html'], data['title_so_html'], data['title_es_html'], data['title_sw_html'], data['title_sv_html'], data['title_ta_html'], data['title_bo_html'], data['title_tr_html'], data['title_uk_html'], data['title_ur_html'], data['title_uz_html'], data['title_vi_html'] = paper.get_other_titles("html")
        #     del data['title_af'], data['title_sq'], data['title_am'], data['title_ar'], data['title_hy'], data['title_az'], data['title_bn'], data['title_bs'], data['title_bg'], data['title_ca'], data['title_zh'], data['title_hr'], data['title_cs'], data['title_da'], data['title_nl'], data['title_et'], data['title_fl'], data['title_fi'], data['title_fr'], data['title_ka'], data['title_de'], data['title_el'], data['title_ha'], data['title_he'], data['title_hi'], data['title_hu'], data['title_is'], data['title_id'], data['title_ga'], data['title_it'], data['title_ja'], data['title_jv'], data['title_kk'], data['title_ko'], data['title_lt'], data['title_mk'], data['title_ms'], data['title_ml'], data['title_mt'], data['title_mn'], data['title_no'], data['title_fa'], data['title_pl'], data['title_pt'], data['title_ro'], data['title_ru'], data['title_sr'], data['title_si'], data['title_sk'], data['title_so'], data['title_es'], data['title_sw'], data['title_sv'], data['title_ta'], data['title_bo'], data['title_tr'], data['title_uk'], data['title_ur'], data['title_uz'], data['title_vi']
        if "xml_booktitle" in data:
            data["booktitle_html"] = paper.get_booktitle("html")
            del data["xml_booktitle"]
        if "abstract" in data:
            data["abstract_html"] = paper.get_abstract("html")
            del data["abstract"]
        # if 'abstract_ar' in data:
        #     data['abstract_af_html'], data['abstract_sq_html'], data['abstract_am_html'], data['abstract_ar_html'], data['abstract_hy_html'], data['abstract_az_html'], data['abstract_bn_html'], data['abstract_bs_html'], data['abstract_bg_html'], data['abstract_ca_html'], data['abstract_zh_html'], data['abstract_hr_html'], data['abstract_cs_html'], data['abstract_da_html'], data['abstract_nl_html'], data['abstract_et_html'], data['abstract_fl_html'], data['abstract_fi_html'], data['abstract_fr_html'], data['abstract_ka_html'], data['abstract_de_html'], data['abstract_el_html'], data['abstract_ha_html'], data['abstract_he_html'], data['abstract_hi_html'], data['abstract_hu_html'], data['abstract_is_html'], data['abstract_id_html'], data['abstract_ga_html'], data['abstract_it_html'], data['abstract_ja_html'], data['abstract_jv_html'], data['abstract_kk_html'], data['abstract_ko_html'], data['abstract_lt_html'], data['abstract_mk_html'], data['abstract_ms_html'], data['abstract_ml_html'], data['abstract_mt_html'], data['abstract_mn_html'], data['abstract_no_html'], data['abstract_fa_html'], data['abstract_pl_html'], data['abstract_pt_html'], data['abstract_ro_html'], data['abstract_ru_html'], data['abstract_sr_html'], data['abstract_si_html'], data['abstract_sk_html'], data['abstract_so_html'], data['abstract_es_html'], data['abstract_sw_html'], data['abstract_sv_html'], data['abstract_ta_html'], data['abstract_bo_html'], data['abstract_tr_html'], data['abstract_uk_html'], data['abstract_ur_html'], data['abstract_uz_html'], data['abstract_vi_html'] = paper.get_other_abstracts("html")
        #     del data['abstract_af'], data['abstract_sq'], data['abstract_am'], data['abstract_ar'], data['abstract_hy'], data['abstract_az'], data['abstract_bn'], data['abstract_bs'], data['abstract_bg'], data['abstract_ca'], data['abstract_zh'], data['abstract_hr'], data['abstract_cs'], data['abstract_da'], data['abstract_nl'], data['abstract_et'], data['abstract_fl'], data['abstract_fi'], data['abstract_fr'], data['abstract_ka'], data['abstract_de'], data['abstract_el'], data['abstract_ha'], data['abstract_he'], data['abstract_hi'], data['abstract_hu'], data['abstract_is'], data['abstract_id'], data['abstract_ga'], data['abstract_it'], data['abstract_ja'], data['abstract_jv'], data['abstract_kk'], data['abstract_ko'], data['abstract_lt'], data['abstract_mk'], data['abstract_ms'], data['abstract_ml'], data['abstract_mt'], data['abstract_mn'], data['abstract_no'], data['abstract_fa'], data['abstract_pl'], data['abstract_pt'], data['abstract_ro'], data['abstract_ru'], data['abstract_sr'], data['abstract_si'], data['abstract_sk'], data['abstract_so'], data['abstract_es'], data['abstract_sw'], data['abstract_sv'], data['abstract_ta'], data['abstract_bo'], data['abstract_tr'], data['abstract_uk'], data['abstract_ur'], data['abstract_uz'], data['abstract_vi']
        if "xml_url" in data:
            del data["xml_url"]
        if "author" in data:
            data["author"] = [
                anthology.people.resolve_name(name, id_) for name, id_ in data["author"]
            ]
        if "editor" in data:
            data["editor"] = [
                anthology.people.resolve_name(name, id_) for name, id_ in data["editor"]
            ]
        for abbrev, style in citation_styles.items():
            data[f"citation_{abbrev}"] = paper.as_citation_html(style)
        papers[paper.collection_id][paper.full_id] = data

    # Prepare people index
    people = defaultdict(dict)
    for id_ in anthology.people.personids():
        name = anthology.people.get_canonical_name(id_)
        log.debug("export_anthology: processing person '{}'".format(repr(name)))
        data = name.as_dict()
        data["slug"] = id_
        if id_ in anthology.people.comments:
            data["comment"] = anthology.people.comments[id_]
        if id_ in anthology.people.similar:
            data["similar"] = sorted(anthology.people.similar[id_])
        data["papers"] = sorted(
            anthology.people.get_papers(id_),
            key=lambda p: anthology.papers.get(p).get("year"),
            reverse=True,
        )
        data["coauthors"] = sorted(
            [[co_id, count] for (co_id, count) in anthology.people.get_coauthors(id_)],
            key=lambda p: p[1],
            reverse=True,
        )
        data["venues"] = sorted(
            [
                [venue, count]
                for (venue, count) in anthology.people.get_venues(
                    anthology.venues, id_
                ).items()
            ],
            key=lambda p: p[1],
            reverse=True,
        )
        variants = [
            n
            for n in anthology.people.get_used_names(id_)
            if n.first != name.first or n.last != name.last
        ]
        if len(variants) > 0:
            data["variant_entries"] = [name.as_dict() for name in sorted(variants)]
        people[id_[0]][id_] = data

    # Prepare volume index
    volumes = {}
    for id_, volume in anthology.volumes.items():
        log.debug("export_anthology: processing volume '{}'".format(id_))
        data = volume.as_dict()
        data["title_html"] = volume.get_title("html")
        del data["xml_booktitle"]
        if "xml_abstract" in data:
            del data["xml_abstract"]
        if "xml_url" in data:
            del data["xml_url"]
        data["has_abstracts"] = volume.has_abstracts
        data["papers"] = volume.paper_ids
        if "author" in data:
            data["author"] = [
                anthology.people.resolve_name(name, id_) for name, id_ in data["author"]
            ]
        if "editor" in data:
            data["editor"] = [
                anthology.people.resolve_name(name, id_) for name, id_ in data["editor"]
            ]
        volumes[volume.full_id] = data

    class SortedVolume:
        """Keys for sorting volumes so they appear in a more reasonable order.
        Takes the parent venue being sorted under, along with its letter,
        and the Anthology ID of the current volume. For example, LREC 2020
        has the following joint events, which get sorted in the following manner:

        ['2020.lrec-1', '2020.aespen-1', '2020.ai4hi-1',
        '2020.bucc-1', '2020.calcs-1', '2020.cllrd-1', '2020.clssts-1',
        '2020.cmlc-1', '2020.computerm-1', '2020.framenet-1', '2020.gamnlp-1',
        '2020.globalex-1', '2020.isa-1', '2020.iwltp-1',
        '2020.ldl-1', '2020.lincr-1', '2020.lr4sshoc-1', '2020.lt4gov-1',
        '2020.lt4hala-1 ', '2020.multilingualbio-1', '2020.onion-1',
        '2020.osact-1', '2020.parlaclarin-1', '2020.rail-1', '2020.readi-1',
        '2020.restup-1', '2020.sltu-1 ', '2020.stoc-1', '2020.trac-1',
        '2020.wac-1', '2020.wildre-1']
        """

        def __init__(self, acronym, letter, anth_id):
            self.parent_venue = acronym.lower()
            self.anth_id = anth_id

            collection_id, self.volume_id, _ = deconstruct_anthology_id(anth_id)
            if is_newstyle_id(collection_id):
                self.venue = collection_id.split(".")[1]
                self.is_parent_venue = self.venue == self.parent_venue
            else:
                self.venue = collection_id[0]
                self.is_parent_venue = self.venue == letter

        def __str__(self):
            return self.anth_id

        def __eq__(self, other):
            """We define equivalence at the venue (not volume) level in order
            to preserve the sort order found in the XML"""
            return self.venue == other.venue

        def __lt__(self, other):
            """First parent volumes, then sort by venue name"""
            if self.is_parent_venue == other.is_parent_venue:
                return self.venue < other.venue
            return self.is_parent_venue and not other.is_parent_venue

    # Prepare venue index
    venues = {}
    for acronym, data in anthology.venues.items():
        letter = data.get("oldstyle_letter", "W")
        data = data.copy()
        data["volumes_by_year"] = {
            year: sorted(
                filter(lambda k: volumes[k]["year"] == year, data["volumes"]),
                key=lambda x: SortedVolume(acronym, letter, x),
            )
            for year in sorted(data["years"])
        }
        data["years"] = sorted(list(data["years"]))
        del data["volumes"]
        venues[acronym] = data

    # Prepare SIG index
    sigs = {}
    for acronym, sig in anthology.sigs.items():
        data = {
            "name": sig.name,
            "slug": sig.slug,
            "url": sig.url,
            "volumes_by_year": sig.volumes_by_year,
            "years": sorted([str(year) for year in sig.years]),
        }
        sigs[acronym] = data

    # Dump all
    if not dryrun:
        # Create directories
        for subdir in ("", "papers", "people"):
            target_dir = "{}/{}".format(outdir, subdir)
            if not check_directory(target_dir, clean=clean):
                return

        progress = tqdm(total=len(papers) + len(people) + 7)
        for collection_id, paper_list in papers.items():
            with open("{}/papers/{}.yaml".format(outdir, collection_id), "w", encoding="utf-8") as f:
                try:
                    yaml.dump(paper_list, Dumper=Dumper, stream=f)
                except:
                    breakpoint()
                    print(collection_id) 
                    sys.exit()
            progress.update()

        with open("{}/volumes.yaml".format(outdir), "w") as f:
            yaml.dump(volumes, Dumper=Dumper, stream=f)
        progress.update(5)

        with open("{}/venues.yaml".format(outdir), "w") as f:
            yaml.dump(venues, Dumper=Dumper, stream=f)
        progress.update()

        with open("{}/sigs.yaml".format(outdir), "w") as f:
            yaml.dump(sigs, Dumper=Dumper, stream=f)
        progress.update()

        for first_letter, people_list in people.items():
            with open("{}/people/{}.yaml".format(outdir, first_letter), "w") as f:
                yaml.dump(people_list, Dumper=Dumper, stream=f)
            progress.update()
        progress.close()


if __name__ == "__main__":
    args = docopt(__doc__)
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    if "{scriptdir}" in args["--importdir"]:
        args["--importdir"] = os.path.abspath(
            args["--importdir"].format(scriptdir=scriptdir)
        )
    if "{scriptdir}" in args["--exportdir"]:
        args["--exportdir"] = os.path.abspath(
            args["--exportdir"].format(scriptdir=scriptdir)
        )

    log_level = log.DEBUG if args["--debug"] else log.INFO
    log.basicConfig(format="%(levelname)-8s %(message)s", level=log_level)
    tracker = SeverityTracker()
    log.getLogger().addHandler(tracker)

    log.info("Reading the Anthology data...")
    anthology = Anthology(importdir=args["--importdir"])
    log.info("Exporting to YAML...")
    export_anthology(
        anthology, args["--exportdir"], clean=args["--clean"], dryrun=args["--dry-run"]
    )

    if tracker.highest >= log.ERROR:
        exit(1)
