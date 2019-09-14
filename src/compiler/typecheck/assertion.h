// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
#pragma once

#include "compiler/ast.h"

namespace verona::compiler
{
  /**
   * Check whether a static assertion holds.
   *
   * If it doesn't, an error is reported in the context and false is returned.
   */
  bool
  check_static_assertion(Context& context, const StaticAssertion& assertion);
}
