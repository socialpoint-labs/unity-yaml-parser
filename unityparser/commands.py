import re
from argparse import ArgumentParser
from multiprocessing import Pool, Manager, Process
from pathlib import Path

from .utils import UnityDocument

YAML_HEADER = '%YAML'


class UnityProjectTester:
    """
    Class to run tests on a given Unity project folder
    """
    AVAILABLE_COMMANDS = ('test_no_yaml_is_modified',)

    def __init__(self):
        self.options = None

    def run(self):
        top_parser = ArgumentParser()
        subparser = top_parser.add_subparsers()
        subparser.required = True
        for cmd in UnityProjectTester.AVAILABLE_COMMANDS:
            fn = getattr(self, cmd)
            parser = subparser.add_parser(cmd, help=fn.__doc__)
            parser.set_defaults(func=fn)
        top_parser.add_argument('project_path', help='Path to the Unity project folder')
        top_parser.add_argument('--exclude',
                                help='Exclude regexp when searching project files. Can be specified multiple times.',
                                default=None,
                                action='append')
        top_parser.add_argument('--keep-changes',
                                help='If a file changes after serialization, do not revert the changes.',
                                default=False,
                                action='store_true')
        top_parser.add_argument('--dry-run',
                                help='Dont\'t modify.',
                                default=False,
                                action='store_true')
        try:
            self.options = top_parser.parse_args()
        except TypeError:
            top_parser.print_help()
            return 2
        # run given function
        self.options.func()

    def test_no_yaml_is_modified(self):
        """
        Recurse the whole project folder looking for '.asset' files, load and save them all, and check that
        there are no modifications
        """
        if self.options.dry_run:
            print("Dry-run mode enabled: YAMLs won't be dumped.")
            if self.options.keep_changes:
                print("Keep changes mode will not have any effect during dry run.")
        elif self.options.keep_changes:
            print("Keep changes mode enabled: Changes to files will be kept.")

        project_path = Path(self.options.project_path)
        asset_file_paths = [p for p in project_path.rglob('*.asset')]
        print("Found {} '.asset' files".format(len(asset_file_paths)))

        def is_path_included(path):
            # compare regexp against absolute path
            return not any(rexp.search(str(path.resolve())) for rexp in rexps)

        if self.options.exclude is not None:
            rexps = [re.compile(rexp) for rexp in self.options.exclude]
            valid_file_paths = [p for p in filter(is_path_included, asset_file_paths)]
            print("Excluded {} '.asset' files".format(len(asset_file_paths) - len(valid_file_paths)))
        else:
            valid_file_paths = asset_file_paths

        file_results = []
        with Manager() as manager:
            print_queue = manager.Queue()
            diff_list = manager.list()
            queue_process = Process(target=UnityProjectTester.read_output, args=(print_queue,))
            queue_process.start()
            with Pool() as pool:
                for f in valid_file_paths:
                    async_res = pool.apply_async(UnityProjectTester.open_and_save,
                                                 (f, print_queue, diff_list, self.options.keep_changes,
                                                  self.options.dry_run))
                    file_results.append((f, async_res))
                pool.close()
                pool.join()
            # signal end of queue with None token
            print_queue.put(None)
            queue_process.join()

            error_results = list(filter(lambda r: not r[1].successful(), file_results))
            if len(error_results):
                # raise the first exception
                file_path, result = error_results[0]
                print("Python process evaluating file {} failed with the following exception:".format(
                    file_path.resolve()), flush=True)
                result.get()
            if len(diff_list):
                print("{} files are different now:".format(len(diff_list)))
                print('\n'.join([str(f.resolve()) for f in diff_list]))

    @staticmethod
    def read_output(print_queue):
        msg = print_queue.get()
        while msg is not None:
            print(msg, flush=True)
            msg = print_queue.get()

    @staticmethod
    def open_and_save(asset_file_path, print_queue, diff_list, keep_changes=False, dry_run=False):
        # check YAML version header, save original content
        with open(str(asset_file_path), 'rb') as fp:
            header = fp.read(len(YAML_HEADER))
            try:
                is_yaml_file = header.decode('utf-8') == YAML_HEADER
            except UnicodeDecodeError:
                is_yaml_file = False
            finally:
                if not is_yaml_file:
                    print_queue.put("Ignoring non-yaml file {}".format(asset_file_path))
                    return
                else:
                    fp.seek(0)
                    print_queue.put("Processing {}".format(asset_file_path))
            a_file_content = fp.read()
        doc = UnityDocument.load_yaml(str(asset_file_path))

        if dry_run:
            return

        try:
            doc.dump_yaml()
            with open(str(asset_file_path), 'rb') as fp:
                b_file_content = fp.read()

            # compare
            if a_file_content != b_file_content:
                diff_list.append(asset_file_path)
                if not keep_changes:
                    with open(str(asset_file_path), 'wb') as fp:
                        fp.write(a_file_content)

        except Exception:
            with open(str(asset_file_path), 'wb') as fp:
                fp.write(a_file_content)
            raise


if __name__ == '__main__':
    # None is considered successful
    code = UnityProjectTester().run() or 0
    exit(code)
