# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# The following guidelines are specific to BZR, GIT, HG and SVN packages.
# Other VCS sources are not natively supported by makepkg yet.

# Maintainer: Your Name <youremail@domain.com>
pkgname=snakes-git # '-bzr', '-git', '-hg' or '-svn'
pkgver=20170406
pkgrel=1
pkgdesc="Snake-based ZPG game"
arch=('x86_64')
url="https://github.com/elan17/snakes-terminalsaver"
license=('GPL')
groups=()
depends=()
makedepends=('git' 'python') # 'bzr', 'git', 'mercurial' or 'subversion'
provides=("${pkgname%-VCS}")
conflicts=("${pkgname%-VCS}")
replaces=()
backup=()
options=(!emptydirs)
install=
source=('snakes-git::git+https://github.com/elan17/snakes-terminalsaver#branch=master')
noextract=()
md5sums=('SKIP')

# Please refer to the 'USING VCS SOURCES' section of the PKGBUILD man page for
# a description of each element in the source array.

pkgver() {
   date +%Y%m%d
}

package() {
	cd "$srcdir/$pkgname"
  	install -Dm 755 snakes.py "${pkgdir}/usr/bin/snakes"
  	install -Dm 644 snakes.conf "${pkgdir}/usr/share/doc/${pkgname}/snakes.config"
  	install -Dm 644 LICENSE "${pkgdir}/usr/share/doc/${pkgname}/LICENSE"
}

